from rest_framework.test import APIClient


class PrefixedAPIClient(APIClient):
    def __init__(self, prefix="/api/v1", *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)
        self.prefix: str = prefix.rstrip("/")

    def _prepend_prefix(self, path: str) -> str:
        if not path.startswith(self.prefix):
            return f"{self.prefix}{path}"
        return path

    def get(self, path, *args, **kwargs):
        return super().get(self._prepend_prefix(path), *args, **kwargs)

    def post(self, path, *args, **kwargs):
        return super().post(self._prepend_prefix(path), *args, **kwargs)

    def patch(self, path, *args, **kwargs):
        return super().patch(self._prepend_prefix(path), *args, **kwargs)

    def put(self, path, *args, **kwargs):
        return super().put(self._prepend_prefix(path), *args, **kwargs)

    def delete(self, path, *args, **kwargs):
        return super().delete(self._prepend_prefix(path), *args, **kwargs)
