from re import MULTILINE, search

from setuptools import setup

version = ""
with open("cloudflare_scan/__init__.py") as f:
    version = search(
        r'^__version__\s*=\s*[\'"]([^\'"]*)[\'"]', f.read(), MULTILINE
    ).group(1)

if not version:
    raise ValueError("Unable to find version string.")

setup(
    name="cloudflarescan",
    author="alexraskin",
    description="Cloudflare URL Scanner SDK",
    version=version,
    url="https://github.com/alexraskin/cloudflare-url-scan",
    author_email="<root@alexraskin.com>",
    license="Mozilla Public License 2.0",
    keywords=[
        "module",
        "Cloudflare",
        "library",
        "package",
        "python",
        "Cloudflare URL Scanner SDK",
    ],
    long_description_content_type="text/markdown",
    long_description=open("README.md", encoding="utf-8").read(),
    install_requires=["httpx", "yarl"],
    packages=["cloudflare_scan"],
    classifiers=[
        "Programming Language :: Python",
        "Programming Language :: Python :: 3.12",
    ],
)
