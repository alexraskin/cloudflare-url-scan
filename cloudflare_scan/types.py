from typing import TypedDict, Optional, Literal


class Headers(TypedDict):
    Content_Type: str
    Authorization: str


class ScanResult(TypedDict):
    success: bool
    errors: list[str]
    messages: list[dict[str, str]]
    result: dict[str, str, str, str]


class SearchResult(TypedDict):
    success: bool
    messages: list[dict[str, str]]
    result: dict[str, dict[list[str]]]
    next_cursor: str
    errors: list[str]


class RequestBody(TypedDict, total=False):
    url: Optional[str]
    screenshots_resolutions: Optional[list[Literal["desktop", "mobile", "tablet"]]]
    custom_user_agent: Optional[str]
    visibility: Optional[str]
