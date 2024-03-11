from typing import Optional, Literal, Dict

from .types import RequestBody


def create_request_body(
    url: Optional[str],
    screenshots_resolutions: Optional[
        list[Literal["desktop", "mobile", "tablet"]]
    ] = None,
    custom_user_agent: Optional[dict] = None,
    visibility: Optional[Literal["Public", "Unlisted"]] = None,
) -> RequestBody:
    """
    Create the request body for the Cloudflare URL Scanner API.
    """
    body: RequestBody = {}

    body["url"] = url

    if screenshots_resolutions is not None:
        body["screenshotsResolutions"] = screenshots_resolutions

    if custom_user_agent is not None:
        body["customHeaders"] = {"user-agent": custom_user_agent}

    if visibility is not None:
        body["visibility"] = visibility

    return body
