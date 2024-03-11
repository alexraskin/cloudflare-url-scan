from typing import Optional

from yarl import URL
from datetime import datetime


class UrlBuilder:
    def __init__(self, cloudflare_account_id: str) -> None:
        self.cloudflare_account_id: str = cloudflare_account_id
        self.scheme: str = "https"
        self.host: str = "api.cloudflare.com"
        self.base_path: str = "/client/v4/accounts/{}/urlscanner/scan"

    def build_search_url(self, endpoint: str) -> str:
        url: URL = URL.build(
            scheme=self.scheme,
            host=self.host,
            path=self.base_path.format(self.cloudflare_account_id),
            query_string=f"page_hostname={endpoint}",
        )
        return url.human_repr()

    def build_scan_url(self) -> str:
        url: URL = URL.build(
            scheme=self.scheme,
            host=self.host,
            path=self.base_path.format(self.cloudflare_account_id),
        )
        return url.human_repr()

    def build_get_screenshot_url(self, uuid: str, resolution: str) -> str:
        url: URL = URL.build(
            scheme=self.scheme,
            host=self.host,
            path=f"{self.base_path.format(self.cloudflare_account_id)}/{uuid}/screenshot",
            query_string=f"resolution={resolution}",
        )
        return url.human_repr()

    def build_get_har_url(self, uuid: str) -> str:
        url: URL = URL.build(
            scheme=self.scheme,
            host=self.host,
            path=f"{self.base_path.format(self.cloudflare_account_id)}/{uuid}/har",
        )
        return url.human_repr()

    def build_get_scan_url(
        self,
        account_scans: Optional[str] = None,
        date_end: Optional[datetime] = None,
        date_start: Optional[datetime] = None,
        hostname: Optional[str] = None,
        ip: Optional[str] = None,
        limit: Optional[int] = None,
        next_cursor: Optional[str] = None,
        page_hostname: Optional[str] = None,
        page_ip: Optional[str] = None,
        page_path: Optional[str] = None,
        page_url: Optional[str] = None,
        path: Optional[str] = None,
        uuid: Optional[str] = None,
        url: Optional[str] = None,
    ) -> str:
        if date_end:
            date_end = date_end.isoformat()

        if date_start:
            date_start = date_start.isoformat()
        params: dict = {
            "account_scans": account_scans,
            "date_end": date_end,
            "date_start": date_start,
            "hostname": hostname,
            "ip": ip,
            "limit": limit,
            "next_cursor": next_cursor,
            "page_hostname": page_hostname,
            "page_ip": page_ip,
            "page_path": page_path,
            "page_url": page_url,
            "path": path,
            "scanId": uuid,
            "url": url,
        }
        filtered_params: dict = {k: v for k, v in params.items() if v is not None}
        url: URL = URL.build(
            scheme=self.scheme,
            host=self.host,
            path=self.base_path.format(self.cloudflare_account_id),
        ).with_query(filtered_params)
        return url.human_repr()
