import httpx

from .types import ScanResult


class CloudflareURLScanResponse:
    """
    Wrapper around the response from the Cloudflare URL Scanner API.
    """

    def __init__(self, response: httpx.Response) -> None:
        self.data = response

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
