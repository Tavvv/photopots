#!/usr/bin/env python3
"""Crawl every .html under website/, extract internal href/src, report missing targets."""
import os, re, sys, html
from urllib.parse import urldefrag

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
ATTR = re.compile(r'''(?:href|src)\s*=\s*["']([^"']+)["']''', re.I)

def resolve(base_file, link):
    link = html.unescape(link).strip()
    if not link or link.startswith(('http://', 'https://', 'mailto:', 'tel:', '#', 'data:', 'javascript:')):
        return None
    link = urldefrag(link)[0]
    if not link:
        return None
    if link.startswith('/'):
        target = os.path.join(ROOT, link.lstrip('/'))
    else:
        target = os.path.normpath(os.path.join(os.path.dirname(base_file), link))
    return target

def exists(target):
    if os.path.isfile(target):
        return True
    # pretty-URL directory: /foo/ -> foo/index.html
    if os.path.isdir(target):
        return os.path.isfile(os.path.join(target, 'index.html'))
    if target.endswith('/'):
        return os.path.isfile(os.path.join(target, 'index.html'))
    return False

broken = []
checked = 0
for dirpath, _, files in os.walk(ROOT):
    if '/tools' in dirpath:
        continue
    for f in files:
        if not f.endswith('.html'):
            continue
        path = os.path.join(dirpath, f)
        rel = os.path.relpath(path, ROOT)
        with open(path, encoding='utf-8') as fh:
            content = fh.read()
        for m in ATTR.finditer(content):
            link = m.group(1)
            t = resolve(path, link)
            if t is None:
                continue
            checked += 1
            if not exists(t):
                broken.append((rel, link, os.path.relpath(t, ROOT)))

print(f"Checked {checked} internal references.")
if broken:
    print(f"\nBROKEN ({len(broken)}):")
    for rel, link, t in broken:
        print(f"  {rel}: {link}  ->  {t}")
    sys.exit(1)
print("All internal references resolve.")
