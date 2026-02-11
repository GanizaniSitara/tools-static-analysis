#!/usr/bin/env python3
"""Screenshot each tab of the viewer using Playwright."""
import sys, os
from playwright.sync_api import sync_playwright

viewer_path = sys.argv[1] if len(sys.argv) > 1 else "output-orchardcore/viewer.html"
url = f"file://{os.path.abspath(viewer_path)}"

with sync_playwright() as p:
    browser = p.chromium.launch()
    page = browser.new_page(viewport={"width": 1400, "height": 900})
    page.goto(url)
    page.wait_for_timeout(4000)

    tabs = page.query_selector_all(".tab-btn")
    for i, tab in enumerate(tabs):
        label = tab.text_content().strip()
        tab.click()
        page.wait_for_timeout(3000)
        fname = f"screenshot-tab{i+1}.png"
        page.screenshot(path=fname, full_page=True)
        print(f"Tab {i+1} '{label}' -> {fname}")

    browser.close()
