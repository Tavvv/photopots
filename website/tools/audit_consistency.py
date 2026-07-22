#!/usr/bin/env python3
"""Consistency: tokens.css+main.css, config.js before main.js, Google Fonts, data-appstore CTAs."""
import os, re, sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
problems = []
config_src = open(os.path.join(ROOT, 'assets/js/config.js'), encoding='utf-8').read()

for dirpath, _, files in os.walk(ROOT):
    if '/tools' in dirpath:
        continue
    for f in sorted(files):
        if not f.endswith('.html'):
            continue
        path = os.path.join(dirpath, f)
        rel = os.path.relpath(path, ROOT)
        t = open(path, encoding='utf-8').read()
        head = t.split('</head>')[0]
        for css in ('tokens.css', 'main.css'):
            if css not in head:
                problems.append(f"{rel}: missing {css}")
        # order: tokens before main
        ti, mi = head.find('tokens.css'), head.find('main.css')
        if ti != -1 and mi != -1 and ti > mi:
            problems.append(f"{rel}: main.css loaded before tokens.css")
        ci, ji = head.find('config.js'), head.find('main.js')
        if ci == -1:
            problems.append(f"{rel}: missing config.js")
        if ji == -1:
            problems.append(f"{rel}: missing main.js")
        if ci != -1 and ji != -1 and ci > ji:
            problems.append(f"{rel}: main.js loaded before config.js")
        if 'fonts.googleapis.com' not in head:
            problems.append(f"{rel}: missing Google Fonts")
        # hard-coded App Store URLs (config.js is the only allowed home)
        for m in re.finditer(r'href="(https?://[^"]*(?:apps\.apple|appstore|app-store)[^"]*)"', t, re.I):
            problems.append(f"{rel}: hard-coded App Store URL: {m.group(1)}")
        # download CTAs must use data-appstore
        body = t.split('</head>')[1] if '</head>' in t else ''
        for m in re.finditer(r'<a\b[^>]*>([^<]*[Dd]ownload[^<]*)</a>', body):
            if 'data-appstore' not in m.group(0):
                problems.append(f"{rel}: Download CTA missing data-appstore: {m.group(0)[:100]}")

# config.js must actually define the store URL
if 'apps.apple.com' not in config_src and 'appstore' not in config_src.lower():
    problems.append("config.js: no App Store URL defined")

print("Consistency audit:")
if problems:
    print(f"\nPROBLEMS ({len(problems)}):")
    for x in problems:
        print("  " + x)
    sys.exit(1)
print("All pages consistent (css order, js order, fonts, data-appstore).")
