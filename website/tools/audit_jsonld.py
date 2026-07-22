#!/usr/bin/env python3
"""Validate all JSON-LD blocks: parse, check @type, URL existence, FAQ answer/text match."""
import os, re, sys, json, html as ihtml

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
BASE = 'https://www.photopots.com'
problems, checked = [], 0

def url_exists(url):
    if not url.startswith(BASE):
        return True  # external (schema.org, fonts) - skip
    p = url[len(BASE):].lstrip('/')
    if not p:
        return True
    full = os.path.join(ROOT, p)
    if os.path.isfile(full):
        return True
    if p.endswith('/') or os.path.isdir(full):
        return os.path.isfile(os.path.join(full, 'index.html'))
    return os.path.isfile(full)

def walk_urls(node, rel, ctx):
    if isinstance(node, dict):
        for k, v in node.items():
            if k in ('url', 'item', 'image', 'mainEntityOfPage') and isinstance(v, str) and v.startswith('http'):
                if not url_exists(v):
                    problems.append(f"{rel}: {ctx} references missing URL {v}")
            else:
                walk_urls(v, rel, ctx)
    elif isinstance(node, list):
        for v in node:
            walk_urls(v, rel, ctx)

def strip_tags(s):
    return re.sub(r'\s+', ' ', re.sub(r'<[^>]+>', '', ihtml.unescape(s))).strip()

for dirpath, _, files in os.walk(ROOT):
    if '/tools' in dirpath:
        continue
    for f in sorted(files):
        if not f.endswith('.html') or f == 'template.html':
            continue
        path = os.path.join(dirpath, f)
        rel = os.path.relpath(path, ROOT)
        text = open(path, encoding='utf-8').read()
        blocks = re.findall(r'<script\s+type="application/ld\+json"[^>]*>(.*?)</script>', text, re.S | re.I)
        for i, b in enumerate(blocks):
            checked += 1
            try:
                data = json.loads(b)
            except json.JSONDecodeError as e:
                problems.append(f"{rel}: JSON-LD block {i} invalid JSON: {e}")
                continue
            graph = data.get('@graph', [data]) if isinstance(data, dict) else data
            for node in graph:
                t = node.get('@type') if isinstance(node, dict) else None
                if not t:
                    problems.append(f"{rel}: JSON-LD node missing @type")
                    continue
                walk_urls(node, rel, t)
                if t == 'BreadcrumbList':
                    for el in node.get('itemListElement', []):
                        item = el.get('item', '')
                        if item.startswith(BASE):
                            p = item[len(BASE):]
                            if p and not p.endswith('/') and not p.endswith('.html'):
                                problems.append(f"{rel}: breadcrumb URL lacks trailing slash: {item}")
                            if p.endswith('.html') and p == '/blog.html':
                                problems.append(f"{rel}: breadcrumb still uses blog.html")
                if t == 'FAQPage':
                    # every Question name + answer text must appear in visible copy
                    visible = strip_tags(re.sub(r'<script.*?</script>', '', text, flags=re.S))
                    for q in node.get('mainEntity', []):
                        qname = strip_tags(q.get('name', ''))
                        ans = q.get('acceptedAnswer', {}).get('text', '')
                        ans_txt = strip_tags(ans)
                        if qname and qname not in visible:
                            problems.append(f"{rel}: FAQPage question not in visible copy: {qname[:70]}")
                        if ans_txt and ans_txt not in visible:
                            problems.append(f"{rel}: FAQPage answer not in visible copy: {ans_txt[:70]}...")

print(f"Parsed {checked} JSON-LD blocks.")
if problems:
    print(f"\nPROBLEMS ({len(problems)}):")
    for x in problems:
        print("  " + x)
    sys.exit(1)
print("JSON-LD validation clean.")
