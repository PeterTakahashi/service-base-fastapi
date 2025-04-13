from asyncio import Event, Lock
from typing import List

from PIL import Image
from pydantic import BaseModel

from manga_translator import Config
from server.sent_data_internal import fetch_data_stream, NotifyType, fetch_data

class ExecutorInstance(BaseModel):
    busy: bool = False
    base_url: str = "http://localhost:8001"

    def free_executor(self):
        self.busy = False

    async def sent(self, image: Image, config: Config):
        url = f"{self.base_url}/simple_execute/translate"
        return await fetch_data(url, image, config)

    async def sent_stream(self, image: Image, config: Config, sender: NotifyType):
        url = f"{self.base_url}/execute/translate"
        await fetch_data_stream(url, image, config, sender)

class Executors:
    def __init__(self):
        self.list: List[ExecutorInstance] = [ExecutorInstance()]
        self.lock: Lock = Lock()
        self.event = Event()

    def free_executors(self) -> int:
        return len([item for item in self.list if not item.busy])

    async def _find_instance(self):
        while True:
            instance = next((x for x in self.list if x.busy == False), None)
            if instance is not None:
                return instance
            await self.event.wait()

    async def find_executor(self) -> ExecutorInstance:
        async with self.lock: # Using async with for lock management
            instance = await self._find_instance()
            instance.busy = True
            return instance

    async def free_executor(self, instance: ExecutorInstance):
        from server.myqueue import task_queue
        instance.free_executor()
        self.event.set()
        self.event.clear()
        await task_queue.update_event()

executor_instances: Executors = Executors()
