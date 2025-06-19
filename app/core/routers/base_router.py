from fastapi import APIRouter


class BaseRouter(APIRouter):

    def get_default_responses(self, request_path: str) -> dict:
        return {}

    def get_full_path(self, path: str) -> str:
        if not self.prefix:
            return path
        return f"{self.prefix.rstrip('/')}{path}"

    def add_api_route(self, path: str, endpoint, *, responses=None, **kwargs):
        default_responses = self.get_default_responses(
            request_path=self.get_full_path(path)
        )

        merged = {**default_responses, **(responses or {})}
        super().add_api_route(path, endpoint, responses=merged, **kwargs)
