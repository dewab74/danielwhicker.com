#!/usr/bin/env python3
"""Tell IndexNow search engines about pages that changed in the last two days.

The addresses come from the live sitemap, so only public pages are ever sent.
`--all` sends every address; `--dry-run` only lists what would be sent.

The key is the name of the 32-character .txt file in the site root. IndexNow
requires it to be public: it only proves that the sender controls the site.
"""

import datetime as dt
import json
import pathlib
import re
import sys
import urllib.error
import urllib.request
import xml.etree.ElementTree as ET

HOST = "danielwhicker.com"
SITEMAP = f"https://{HOST}/sitemap.xml"
ENDPOINT = "https://api.indexnow.org/indexnow"
WINDOW = dt.timedelta(days=2)
NS = "{http://www.sitemaps.org/schemas/sitemap/0.9}"
AGENT = {"User-Agent": "site-indexnow-notifier"}


def site_key():
    root = pathlib.Path(__file__).resolve().parent.parent
    found = [p.stem for p in root.glob("*.txt") if re.fullmatch(r"[0-9a-f]{32}", p.stem)]
    if len(found) != 1:
        sys.exit("expected exactly one IndexNow key file in the site root")
    return found[0]


def addresses(sitemap, everything, now):
    urls = []
    for entry in ET.fromstring(sitemap).iter(f"{NS}url"):
        location = entry.findtext(f"{NS}loc")
        changed = entry.findtext(f"{NS}lastmod")
        recent = changed and now - dt.datetime.fromisoformat(changed) <= WINDOW
        if location and (everything or recent):
            urls.append(location)
    return urls


def main():
    args = set(sys.argv[1:])
    if args - {"--all", "--dry-run"}:
        sys.exit(__doc__)
    request = urllib.request.Request(SITEMAP, headers=AGENT)
    with urllib.request.urlopen(request, timeout=30) as response:
        sitemap = response.read()
    urls = addresses(sitemap, "--all" in args, dt.datetime.now(dt.timezone.utc))
    if not urls:
        print("nothing new to announce")
        return 0
    print("\n".join(urls))
    if "--dry-run" in args:
        return 0

    key = site_key()
    body = {
        "host": HOST,
        "key": key,
        "keyLocation": f"https://{HOST}/{key}.txt",
        "urlList": urls,
    }
    request = urllib.request.Request(
        ENDPOINT,
        data=json.dumps(body).encode(),
        headers={**AGENT, "Content-Type": "application/json; charset=utf-8"},
    )
    try:
        with urllib.request.urlopen(request, timeout=30) as response:
            print(f"IndexNow accepted {len(urls)} address(es): HTTP {response.status}")
    except urllib.error.HTTPError as error:
        print(f"IndexNow refused the request: HTTP {error.code} {error.reason}")
        return 1
    return 0


if __name__ == "__main__":
    sys.exit(main())
