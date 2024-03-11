import httpx

from .types import ScanResult


class CloudflareURLScanResponse:
    """
    Cloudflare URL Scanner API Response object.
    """

    def __init__(self, response: httpx.Response) -> None:
        self.data = response

    def __str__(self) -> str:
        return f"CloudflareURLScanResponse(status_code={self.status_code})"

    def __repr__(self) -> str:
        return f"CloudflareURLScanResponse(status_code={self.status_code})"

    def __bool__(self) -> bool:
        return self.success

    def __iter__(self):
        return iter(self.json)

    def __getitem__(self, key):
        return self.json[key]

    @property
    def json(self) -> dict:
        return self.data.json()

    @property
    def text(self) -> str:
        return self.data.text

    @property
    def status_code(self) -> int:
        return self.data.status_code

    @property
    def headers(self) -> dict[str, str]:
        return self.data.headers

    @property
    def errors(self) -> list[str]:
        return self.json.get("errors", [])

    @property
    def messages(self) -> list[dict[str, str]]:
        return self.json.get("messages", [])

    @property
    def result(self) -> ScanResult:
        return self.json.get("result", {})

    @property
    def uuid(self) -> str:
        return self.result.get("result", {}).get("uuid", "")

    @property
    def success(self) -> bool:
        return self.json.get("success", False)

    @property
    def tasks(self) -> list[str]:
        return self.json.get("result", {}).get("tasks", [])
