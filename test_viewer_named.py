#!/usr/bin/env python3
"""Screenshot overview + first category tab for multiple viewers."""
import sys, os
from playwright.sync_api import sync_playwright

viewers = sys.argv[1:] if len(sys.argv) > 1 else []

with sync_playwright() as p:
    browser = p.chromium.launch()
    for viewer_path in viewers:
        name = os.path.basename(os.path.dirname(viewer_path))
        url = f"file://{os.path.abspath(viewer_path)}"
        page = browser.new_page(viewport={"width": 1400, "height": 900})
        page.goto(url)
        page.wait_for_timeout(4000)
        page.screenshot(path=f"ss-{name}-overview.png", full_page=True)

        tabs = page.query_selector_all(".tab-btn")
        if len(tabs) > 1:
            tabs[1].click()
            page.wait_for_timeout(3000)
            label = tabs[1].text_content().strip().split()[0].lower()
            page.screenshot(path=f"ss-{name}-{label}.png", full_page=True)
        page.close()
    browser.close()
