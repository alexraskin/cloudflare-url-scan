# Cloudflare URL Scanner PY-SDK

Python SDK for the Cloudflare URL Scanner API. It provides a simple way to interact with the API and scan URLs for malware, phishing, and more. To better understand Internet usage around the world, use Cloudflare’s URL Scanner. With Cloudflare’s URL Scanner, you have the ability to investigate the details of a domain, IP, URL, or ASN. Cloudflare’s URL Scanner is available in the Security Center of the Cloudflare dashboard, [Cloudflare Radar](https://radar.cloudflare.com/scan) and the [Cloudflare API](https://developers.cloudflare.com/api/operations/urlscanner-search-scans).

Read more about the Cloudflare URL Scanner API [here](https://developers.cloudflare.com/radar/investigate/url-scanner/).

> [!NOTE]
> This SDK is **not** an official Cloudflare product.

> [!NOTE]
> By default, the report will have a Public visibility level, which means it will appear in the recent scans list and in search results. It will also include a single screenshot with desktop resolution.

## Features

- Scan a URL
- Get the scan result
- Search for a scan by hostname
- Search for a scan by UUID
- Many more
- Async support

## Installation

From pip:

```bash
pip install cloudflarescan
```

From github:

```bash
python -m pip install -U git+https://github.com/alexraskin/cloudflare-url-scan
```

From source:

```bash
git clone
cd cloudflare-url-scan
python -m pip install .
```

## Usage

To make your first URL scan using the API, you must obtain a URL Scanner specific [API token](https://developers.cloudflare.com/fundamentals/api/get-started/create-token/). Create a Custom Token with Account > URL Scanner in the Permissions group, and select Edit as the access level.

```python
from cloudflare_scan import UrlScannerClient


cf_client = Client(
    cloudflare_api_key="", #or set the environment variable CLOUDFLARE_API_KEY
    cloudflare_account_id="", #or set the environment variable CLOUDFLARE_ACCOUNT_ID
)

# Scan a URL
scan = cf_client.scan("example.com")

# Get the scan result
result = scan.result

# Get the UUID of the scan
uuid = scan.uuid

# Get the screenshot of the scan
screenshot = cf_client.get_screen_shots(uuid, resolution="desktop")

# Get the HAR file of the scan
har = cf_client.get_har(uuid)

# Get the scan by UUID
scan = cf_client.get_scan(uuid)
```

## Async Usage

```python
from cloudflare_scan import AsyncClient
import asyncio

cf_client = AsyncClient(
    cloudflare_api_key="",
    cloudflare_account_id=""
    )

async def main():
    scan = await cf_client.scan("https://www.google.com")
    print(scan.result)
    print(scan.json)

asyncio.run(main())
```

## License

MIT License [LICENSE]
