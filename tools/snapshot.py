#!/usr/bin/env python3
"""One-off: mirror the four source pages and the assets they reference into snap/."""
import os, re, sys, urllib.request, urllib.parse

UA = "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/126.0 Safari/537.36"
SITE = "https://biketoursofsb.com"
PAGES = {"home": "/", "our-story": "/our-story/", "faq": "/faq/", "contact-us": "/contact-us/",
         "available-bikes": "/available-bikes/",
         "choosing-a-bike": "/choosing-a-bike-for-your-bike-tour-of-santa-barbara/",
         "getting-the-most": "/how-to-get-the-most-out-of-your-bike-tour-of-santa-barbara/",
         "ways-to-tour": "/ways-to-tour-santa-barbra-on-bike/"}
EXT = (".css", ".png", ".jpg", ".jpeg", ".webp", ".svg", ".gif", ".woff", ".woff2", ".ttf", ".avif", ".ico")
OUT = "snap"
seen, failed = {}, []

def get(url):
    req = urllib.request.Request(url, headers={"User-Agent": UA, "Accept": "*/*"})
    with urllib.request.urlopen(req, timeout=40) as r:
        return r.read()

def local(url):
    u = urllib.parse.urlsplit(url)
    return os.path.join(OUT, "files", u.netloc, urllib.parse.unquote(u.path).lstrip("/"))

def save(path, data):
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, "wb") as f:
        f.write(data)

def fetch(url):
    url = url.split("#")[0]
    if url in seen:
        return seen[url]
    seen[url] = None
    try:
        data = get(url)
    except Exception as e:
        failed.append(f"{url} :: {e}")
        return None
    path = local(url)
    if path.endswith("/") or not os.path.splitext(path)[1]:
        path = path.rstrip("/") + ".css"
    save(path, data)
    seen[url] = path
    if path.endswith(".css"):
        text = data.decode("utf-8", "replace")
        for m in re.finditer(r"url\(\s*['\"]?([^'\")]+)['\"]?\s*\)", text):
            ref = m.group(1).strip()
            if ref.startswith("data:"):
                continue
            absu = urllib.parse.urljoin(url, ref)
            if urllib.parse.urlsplit(absu).path.lower().endswith(EXT):
                fetch(absu)
    return path

def refs(html):
    html = html.replace("\\/", "/").replace("&amp;", "&")
    found = set()
    for m in re.finditer(r"https?://[^\s\"'<>()\\,]+", html):
        u = m.group(0)
        p = urllib.parse.urlsplit(u)
        if p.path.lower().endswith(EXT) and (p.netloc.endswith("biketoursofsb.com") or p.path.lower().endswith(".css")):
            found.add(u)
        if p.netloc == "fonts.googleapis.com":
            found.add(u)
    return found

def main():
    for sm in ("/robots.txt", "/sitemap_index.xml", "/wp-sitemap.xml", "/page-sitemap.xml", "/post-sitemap.xml"):
        try:
            save(os.path.join(OUT, "meta", sm.strip("/")), get(SITE + sm))
        except Exception as e:
            failed.append(f"{SITE + sm} :: {e}")
    for name, path in PAGES.items():
        try:
            data = get(SITE + path)
        except Exception as e:
            print(f"::error::{name}: {e}")
            sys.exit(1)
        save(os.path.join(OUT, "pages", name + ".html"), data)
        html = data.decode("utf-8", "replace")
        urls = refs(html)
        print(f"::notice::{name}: {len(data)} bytes, {len(urls)} asset refs")
        for u in sorted(urls):
            fetch(u)
    ok = [v for v in seen.values() if v]
    size = sum(os.path.getsize(p) for p in ok)
    print(f"::notice::saved {len(ok)} files, {size // 1024} KB, {len(failed)} failed")
    save(os.path.join(OUT, "failed.txt"), "\n".join(failed).encode())
    save(os.path.join(OUT, "manifest.txt"), "\n".join(f"{u}\t{p}" for u, p in sorted(seen.items()) if p).encode())

main()
