from typing import TypedDict, Optional, Literal
from datetime import datetime


class ScanResult(TypedDict):
    success: bool
    errors: list[str]
    messages: list[dict[str, str]]
    result: dict[str, str]


class SearchResult(TypedDict):
    success: bool
    messages: list[dict[str, str]]
    result: dict[str, dict[list[str], str]]
    next_cursor: str
    errors: list[str]


class RequestBody(TypedDict, total=False):
    url: Optional[str]
    screenshotsResolutions: Optional[list[Literal["desktop", "mobile", "tablet"]]]
    customHeaders: Optional[dict]
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
