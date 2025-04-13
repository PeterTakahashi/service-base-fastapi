import asyncio
import pickle
from threading import Lock

import uvicorn
from fastapi import FastAPI, HTTPException, Request, Response

from starlette.responses import StreamingResponse

from manga_translator import MangaTranslator

class MangaShare:
    def __init__(self, params: dict = None):
        self.manga = MangaTranslator(params)
        self.host = params.get('host', '127.0.0.1')
        self.port = int(params.get('port', '8001'))
        self.nonce = params.get('nonce', None)

        # each chunk has a structure like this status_code(int/1byte),len(int/4bytes),bytechunk
        # status codes are 0 for result, 1 for progress report, 2 for error
        self.progress_queue = asyncio.Queue()
        self.lock = Lock()

        async def hook(state: str, finished: bool):
            state_data = state.encode("utf-8")
            progress_data = b'\x01' + len(state_data).to_bytes(4, 'big') + state_data
            await self.progress_queue.put(progress_data)
            await asyncio.sleep(0)

        self.manga.add_progress_hook(hook)

    async def progress_stream(self):
        """
        loops until the status is != 1 which is eiter an error or the result
        """
        while True:
            progress = await self.progress_queue.get()
            yield progress
            if progress[0] != 1:
                break

    async def translate_stream(self, **attributes):
        try:
            result = await self.manga.translate(**attributes)
            result_bytes = pickle.dumps(result)
            encoded_result = b'\x00' + len(result_bytes).to_bytes(4, 'big') + result_bytes
            await self.progress_queue.put(encoded_result)
        except Exception as e:
            err_bytes = str(e).encode("utf-8")
            encoded_result = b'\x02' + len(err_bytes).to_bytes(4, 'big') + err_bytes
            await self.progress_queue.put(encoded_result)
        finally:
            self.lock.release()

    def check_nonce(self, request: Request):
        if self.nonce:
            nonce = request.headers.get('X-Nonce')
            if nonce != self.nonce:
                raise HTTPException(401, detail="Nonce does not match")

    def check_lock(self):
        if not self.lock.acquire(blocking=False):
            raise HTTPException(status_code=429, detail="some Method is already being executed.")

    async def listen(self, translation_params: dict = None):
        app = FastAPI(
            title="Manga Translator shared API",
            description="A FastAPI server for manga translation",
            version="1.0.0"
        )

        @app.post("/simple_execute/translate")
        async def simple_execute_translate(request: Request):
            self.check_nonce(request)
            self.check_lock()
            attributes_bytes = await request.body()
            attr = pickle.loads(attributes_bytes)
            try:
                result = await self.manga.translate(**attr)
                self.lock.release()
                result_bytes = pickle.dumps(result)
                return Response(content=result_bytes, media_type="application/octet-stream")
            except Exception as e:
                self.lock.release()
                raise HTTPException(status_code=500, detail=str(e))

        @app.post("/execute/translate")
        async def execute_translate(request: Request):
            self.check_nonce(request)
            self.check_lock()
            attributes_bytes = await request.body()
            attr = pickle.loads(attributes_bytes)

            # streaming response
            streaming_response = StreamingResponse(self.progress_stream(), media_type="application/octet-stream")
            asyncio.create_task(self.translate_stream(**attr))
            return streaming_response

        config = uvicorn.Config(app, host=self.host, port=self.port)
        server = uvicorn.Server(config)
        await server.serve()
