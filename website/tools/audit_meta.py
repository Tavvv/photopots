#!/usr/bin/env python3
"""Audit meta: one h1, unique title <=60, unique description <=155, canonical, OG, Twitter."""
import os, re, sys, json
from collections import Counter

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
pages = []
for dirpath, _, files in os.walk(ROOT):
    if '/tools' in dirpath:
        continue
    for f in files:
        if f.endswith('.html'):
            pages.append(os.path.join(dirpath, f))
pages.sort()

titles, descs, canonicals = {}, {}, {}
problems = []

def grab(pat, text, flags=re.I | re.S):
    m = re.search(pat, text, flags)
    return m.group(1).strip() if m else None

for p in pages:
    rel = os.path.relpath(p, ROOT)
    t = open(p, encoding='utf-8').read()
    if rel == 'template.html':
        continue
    h1s = re.findall(r'<h1[\s>]', t, re.I)
    if len(h1s) != 1:
        problems.append(f"{rel}: {len(h1s)} <h1> tags")
    title = grab(r'<title>(.*?)</title>', t)
    if not title:
        problems.append(f"{rel}: missing <title>")
    else:
        titles.setdefault(title, []).append(rel)
        if len(title) > 60:
            problems.append(f"{rel}: title {len(title)} chars > 60: {title}")
    desc = grab(r'<meta\s+name="description"\s+content="([^"]*)"', t)
    if not desc:
        problems.append(f"{rel}: missing meta description")
    else:
        descs.setdefault(desc, []).append(rel)
        if len(desc) > 155:
            problems.append(f"{rel}: description {len(desc)} chars > 155")
    canon = grab(r'<link\s+rel="canonical"\s+href="([^"]*)"', t)
    if rel == '404.html':
        if canon:
            problems.append(f"{rel}: 404 should have no canonical (found {canon})")
    else:
        if not canon:
            problems.append(f"{rel}: missing canonical")
        elif not canon.startswith('https://www.photopots.com'):
            problems.append(f"{rel}: canonical not on www.photopots.com: {canon}")
        else:
            canonicals.setdefault(canon, []).append(rel)
    for prop in ('og:title', 'og:description', 'og:url', 'og:image'):
        if f'property="{prop}"' not in t:
            problems.append(f"{rel}: missing {prop}")
    for name in ('twitter:card', 'twitter:title', 'twitter:description', 'twitter:image'):
        if f'name="{name}"' not in t:
            problems.append(f"{rel}: missing {name}")

for coll, label in ((titles, 'title'), (descs, 'description'), (canonicals, 'canonical')):
    for val, rs in coll.items():
        if len(rs) > 1:
            problems.append(f"DUPLICATE {label} across {rs}: {val[:90]}")

# canonical <-> on-disk path consistency
for canon, rs in canonicals.items():
    url_path = canon.replace('https://www.photopots.com', '').lstrip('/')
    expect = url_path if url_path.endswith('.html') else os.path.join(url_path, 'index.html')
    expect = expect or 'index.html'
    for r in rs:
        if r != expect:
            problems.append(f"{r}: canonical path mismatch -> {canon}")

print(f"Audited {len(pages)} html files.")
if problems:
    print(f"\nPROBLEMS ({len(problems)}):")
    for x in problems:
        print("  " + x)
    sys.exit(1)
print("Meta audit clean.")
