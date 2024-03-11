import os
import httpx
from datetime import datetime
from typing import Optional, Literal

from .types import Headers
from .builder import UrlBuilder
from .helpers import create_request_body
from .response import CloudflareURLScanResponse


class Client:
    """
    Client to interact with the Cloudflare URL Scanner API.

    Visit https://developers.cloudflare.com/radar/investigate/url-scanner/ for more information.
    """

    def __init__(
        self,
        cloudflare_api_key: Optional[str] = None,
        cloudflare_account_id: Optional[str] = None,
        timeout: Optional[int] = 60,
    ) -> None:
        """
        Parameters:

        cloudflare_api_key : str (optional) will be taken from the environment variable CLOUDFLARE_API_KEY
            The Cloudflare API key.
        cloudflare_account_id : str (optional) will be taken from the environment variable CLOUDFLARE_ACCOUNT_ID
            The Cloudflare account ID.
        timeout : int (optional)
            The timeout for the requests (default is 60 seconds)

        """
        if cloudflare_api_key is None:
            self.cloudflare_api_key = os.getenv("CLOUDFLARE_API_KEY")
        self.cloudflare_api_key = cloudflare_api_key

        if cloudflare_account_id is None:
            self.cloudflare_account_id = os.getenv("CLOUDFLARE_ACCOUNT_ID")
        self.cloudflare_account_id = cloudflare_account_id

        self._timeout = timeout
        self._http_client = httpx.Client(timeout=self._timeout)
        self._url_builder = UrlBuilder(self.cloudflare_account_id)

    def __str__(self) -> str:
        return f"UrlScannerClient(cloudflare_account_id={self.cloudflare_account_id})"

    def __repr__(self) -> str:
        return f"UrlScannerClient(cloudflare_account_id={self.cloudflare_account_id})"

    def _build_headers(self) -> Headers:
        return {
            "Content-Type": "application/json",
            "Authorization": f"Bearer {self.cloudflare_api_key}",
        }

    def _http(
        self,
        method: Literal["GET", "POST"],
        url: str,
        headers: dict[str, str] = None,
        data: dict[str, str] = None,
    ) -> httpx.Response:
        """
        Make an HTTP request to the Cloudflare API.
        """
        if headers is None:
            headers = self._build_headers()
        return self._http_client.request(
            method=method, url=url, headers=headers, json=data
        )

    def scan(
        self,
        url: str,
        screenshots_resolutions: Optional[
            list[Literal["desktop", "mobile", "tablet"]]
        ] = None,
        custom_user_agent: Optional[str] = None,
        visibility: Optional[Literal["Public", "Unlisted"]] = None,
    ) -> CloudflareURLScanResponse:
        """
        Submit a URL to scan. You can also set some options, like the visibility level and custom headers.
        Accounts are limited to 1 new scan every 10 seconds and 8000 per month. If you need more, please reach out.

        Parameters:
        url : str
            The URL to scan.
        screenshots_resolutions : list[str] (optional)
            The resolutions to take screenshots of. Possible values are desktop, mobile, and tablet.
        custom_user_agent : str (optional)
            The user agent to use when scanning the URL.
        visibility : str (optional)
            The visibility level of the scan. Possible values are Public and Unlisted.

        Returns:
        CloudflareURLScanResponse
            The response from the API.
        """
        body = create_request_body(
            url=url,
            screenshots_resolutions=screenshots_resolutions,
            custom_user_agent=custom_user_agent,
            visibility=visibility,
        )
        response = self._http(
            method="POST",
            url=self._url_builder.build_scan_url(),
            data=body,
        )
        return CloudflareURLScanResponse(response=response)

    def get_scan(self, uuid: str) -> CloudflareURLScanResponse:
        """
        Get a scan by UUID.

        Parameters:
        uuid : str
            The UUID of the scan.

        Returns:
        CloudflareURLScanResponse
            The response from the API.
        """
        response = self._http(
            method="GET",
            url=self._url_builder.build_get_scan_url(uuid=uuid),
        )
        return CloudflareURLScanResponse(response=response)

    def get_screen_shots(
        self, uuid: str, resolution: Literal["desktop", "mobile", "table"]
    ) -> CloudflareURLScanResponse:
        """
        Get scan's screenshot by resolution (desktop/mobile/tablet).

        Parameters:
        uuid : str
            The UUID of the scan.
        resolution : str (optional) (default is desktop)

        Returns:
        CloudflareURLScanResponse
            The response from the API.
        """
        response = self._http(
            method="GET",
            url=self._url_builder.build_get_screenshot_url(
                uuid=uuid, resolution=resolution
            ),
        )
        return CloudflareURLScanResponse(response=response)

    def get_har(self, uuid: str) -> CloudflareURLScanResponse:
        """
        Get a URL scan's HAR file. See HAR spec at http://www.softwareishard.com/blog/har-12-spec/.

        Parameters:
        uuid : str
            The UUID of the scan.

        Returns:
        CloudflareURLScanResponse
            The response from the API.
        """
        response = self._http(
            method="GET",
            url=self._url_builder.build_get_har_url(uuid=uuid),
        )
        return CloudflareURLScanResponse(response=response)

    def search(
        self,
        scanId: Optional[str] = None,
        account_scans: Optional[bool] = None,
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
        url: Optional[str] = None,
    ) -> CloudflareURLScanResponse:
        """
        Search scans by date and webpages' requests, including full URL (after redirects), hostname, and path.
        A successful scan will appear in search results a few minutes after finishing but may take much longer if the system in under load.
        By default, only successfully completed scans will appear in search results, unless searching by scanId.
        Please take into account that older scans may be removed from the search index at an unspecified time.

        Parameters:
        scanId: string: <uuid>

        account_scans: boolean: Return only scans created by account.

        date_end: string <date-time>: Filter scans requested before date (inclusive).

        date_start: string <date-time>: Filter scans requested after date (inclusive).

        hostname: string: Filter scans by hostname of any request made by the webpage.

        ip: string: Filter scans by IP address (IPv4 or IPv6) of any request made by the webpage.

        limit: integer: Limit the number of objects in the response.

        next_cursor: string: Pagination cursor to get the next set of results.

        page_hostname: string: Filter scans by main page hostname .

        page_ip: string: Filter scans by main page IP address (IPv4 or IPv6).

        page_path: string: Filter scans by exact match URL path (also supports suffix search).

        page_url: string: Filter scans by exact match to scanned URL (after redirects)

        path: string: Filter scans by url path of any request made by the webpage: Example: /samples/subresource-integrity/

        url: string: Filter scans by exact match URL of any request made by the webpage: Example: https://example.com/?hello

        Returns:
        CloudflareURLScanResponse
            The response from the API.
        """
        url = self._url_builder.build_get_scan_url(
            account_scans=account_scans,
            date_end=date_end,
            date_start=date_start,
            hostname=hostname,
            ip=ip,
            limit=limit,
            next_cursor=next_cursor,
            page_hostname=page_hostname,
            page_ip=page_ip,
            page_path=page_path,
            page_url=page_url,
            path=path,
            uuid=scanId,
            url=url,
        )
        response = self._http(method="GET", url=url)
        return CloudflareURLScanResponse(response=response)


class AsyncClient:
    """
    Async Client to interact with the Cloudflare URL Scanner API.

    Visit https://developers.cloudflare.com/radar/investigate/url-scanner/ for more information.
    """

    def __init__(
        self,
        cloudflare_api_key: Optional[str] = None,
        cloudflare_account_id: Optional[str] = None,
        timeout: Optional[int] = 60,
    ) -> None:
        """
        Parameters:

        cloudflare_api_key : str (optional) will be taken from the environment variable CLOUDFLARE_API_KEY
            The Cloudflare API key.
        cloudflare_account_id : str (optional) will be taken from the environment variable CLOUDFLARE_ACCOUNT_ID
            The Cloudflare account ID.
        timeout : int (optional)
            The timeout for the requests (default is 60 seconds)

        """
        if cloudflare_api_key is None:
            self.cloudflare_api_key = os.getenv("CLOUDFLARE_API_KEY")
        self.cloudflare_api_key = cloudflare_api_key

        if cloudflare_account_id is None:
            self.cloudflare_account_id = os.getenv("CLOUDFLARE_ACCOUNT_ID")
        self.cloudflare_account_id = cloudflare_account_id

        self._timeout = timeout
        self._http_client = httpx.AsyncClient(timeout=self._timeout)
        self._url_builder = UrlBuilder(self.cloudflare_account_id)

    def _build_headers(self) -> Headers:
        return {
            "Content-Type": "application/json",
            "Authorization": f"Bearer {self.cloudflare_api_key}",
        }

    async def _http(
        self,
        method: Literal["GET", "POST"],
        url: str,
        headers: dict[str, str] = None,
        data: dict[str, str] = None,
    ) -> httpx.Response:
        """
        Make an HTTP request to the Cloudflare API.
        """
        if headers is None:
            headers = self._build_headers()
        return await self._http_client.request(
            method=method, url=url, headers=headers, json=data
        )

    async def scan(
        self,
        url: str,
        screenshots_resolutions: Optional[
            list[Literal["desktop", "mobile", "tablet"]]
        ] = None,
        custom_user_agent: Optional[str] = None,
        visibility: Optional[Literal["Public", "Unlisted"]] = None,
    ) -> CloudflareURLScanResponse:
        """
        Submit a URL to scan. You can also set some options, like the visibility level and custom headers.
        Accounts are limited to 1 new scan every 10 seconds and 8000 per month. If you need more, please reach out.

        Parameters:
        url : str
            The URL to scan.
        screenshots_resolutions : list[str] (optional)
            The resolutions to take screenshots of. Possible values are desktop, mobile, and tablet.
        custom_user_agent : str (optional)
            The user agent to use when scanning the URL.
        visibility : str (optional)
            The visibility level of the scan. Possible values are Public and Unlisted.

        Returns:
        CloudflareURLScanResponse
            The response from the API.
        """

        body = create_request_body(
            url=url,
            screenshots_resolutions=screenshots_resolutions,
            custom_user_agent=custom_user_agent,
            visibility=visibility,
        )
        response = await self._http(
            method="POST",
            url=self._url_builder.build_scan_url(),
            data=body,
        )
        return CloudflareURLScanResponse(response=response)

    async def get_scan(self, uuid: str) -> CloudflareURLScanResponse:
        """
        Get a scan by UUID.

        Parameters:
        uuid : str
            The UUID of the scan.

        Returns:
        CloudflareURLScanResponse
            The response from the API.
        """
        response = await self._http(
            method="GET",
            url=self._url_builder.build_get_scan_url(uuid=uuid),
        )
        return CloudflareURLScanResponse(response=response)

    async def get_screen_shots(
        self, uuid: str, resolution: Literal["desktop", "mobile", "table"]
    ) -> CloudflareURLScanResponse:
        """
        Get scan's screenshot by resolution (desktop/mobile/tablet).

        Parameters:
        uuid : str
            The UUID of the scan.
        resolution : str (optional) (default is desktop)

        Returns:
        CloudflareURLScanResponse
            The response from the API.
        """
        response = await self._http(
            method="GET",
            url=self._url_builder.build_get_screenshot_url(
                uuid=uuid, resolution=resolution
            ),
        )
        return CloudflareURLScanResponse(response=response)

    async def get_har(self, uuid: str) -> CloudflareURLScanResponse:
        """
        Get a URL scan's HAR file. See HAR spec at http://www.softwareishard.com/blog/har-12-spec/.

        Parameters:
        uuid : str
            The UUID of the scan.

        Returns:
        CloudflareURLScanResponse
            The response from the API.
        """
        response = await self._http(
            method="GET",
            url=self._url_builder.build_get_har_url(uuid=uuid),
        )
        return CloudflareURLScanResponse(response=response)

    async def search(
        self,
        scanId: Optional[str] = None,
        account_scans: Optional[bool] = None,
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
        url: Optional[str] = None,
    ) -> CloudflareURLScanResponse:
        """
        Search scans by date and webpages' requests, including full URL (after redirects), hostname, and path.
        A successful scan will appear in search results a few minutes after finishing but may take much longer if the system in under load.
        By default, only successfully completed scans will appear in search results, unless searching by scanId.
        Please take into account that older scans may be removed from the search index at an unspecified time.

        Parameters:
        scanId: string: <uuid>

        account_scans: boolean: Return only scans created by account.

        date_end: string <date-time>: Filter scans requested before date (inclusive).

        date_start: string <date-time>: Filter scans requested after date (inclusive).

        hostname: string: Filter scans by hostname of any request made by the webpage.

        ip: string: Filter scans by IP address (IPv4 or IPv6) of any request made by the webpage.

        limit: integer: Limit the number of objects in the response.

        next_cursor: string: Pagination cursor to get the next set of results.

        page_hostname: string: Filter scans by main page hostname .

        page_ip: string: Filter scans by main page IP address (IPv4 or IPv6).

        page_path: string: Filter scans by exact match URL path (also supports suffix search).

        page_url: string: Filter scans by exact match to scanned URL (after redirects)

        path: string: Filter scans by url path of any request made by the webpage: Example: /samples/subresource-integrity/

        url: string: Filter scans by exact match URL of any request made by the webpage: Example: https://example.com/?hello

        Returns:
        CloudflareURLScanResponse
            The response from the API.
        """
        url = self._url_builder.build_get_scan_url(
            account_scans=account_scans,
            date_end=date_end,
            date_start=date_start,
            hostname=hostname,
            ip=ip,
            limit=limit,
            next_cursor=next_cursor,
            page_hostname=page_hostname,
            page_ip=page_ip,
            page_path=page_path,
            page_url=page_url,
            path=path,
            uuid=scanId,
            url=url,
        )
        response = await self._http(method="GET", url=url)
        return CloudflareURLScanResponse(response=response)

    async def close(self) -> None:
        """
        Close the HTTP client session.
        """
        await self._http_client.aclose()
