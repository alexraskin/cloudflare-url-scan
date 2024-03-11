from typing import TypedDict, Optional, Literal
from datetime import datetime


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


class SearchParams:
    account_scans: Optional[str]
    date_end: Optional[datetime]
    date_start: Optional[datetime]
    hostname: Optional[str]
    ip: Optional[str]
    limit: Optional[int]
    next_cursor: Optional[str]
    page_hostname: Optional[str]
    page_ip: Optional[str]
    page_path: Optional[str]
    page_url: Optional[str]
    path: Optional[str]
    uuid: Optional[str]
