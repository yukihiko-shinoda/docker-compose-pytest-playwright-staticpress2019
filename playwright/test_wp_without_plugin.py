#!/usr/bin/env python3
"""Test if WordPress loads without the plugin."""

import os

from dotenv import load_dotenv
from playwright.sync_api import sync_playwright

load_dotenv()

HOST = os.getenv("HOST", "http://localhost/")
BASIC_AUTH_USERNAME = "authuser"
BASIC_AUTH_PASSWORD = "authpassword"

with sync_playwright() as p:
    browser = p.chromium.launch(headless=True)
    context = browser.new_context(
        http_credentials={
            "username": BASIC_AUTH_USERNAME,
            "password": BASIC_AUTH_PASSWORD,
        },
        viewport={"width": 1920, "height": 1080},
    )
    page = context.new_page()

    print("Navigating to WordPress admin...")
    page.goto(HOST + "wp-admin/", wait_until="networkidle")
    page.screenshot(path="wp_admin_no_plugin.png")

    # Check for critical error
    page_text = page.content()
    if "critical error" in page_text.lower():
        print("❌ CRITICAL ERROR DETECTED")
    else:
        print("✓ WordPress admin loaded successfully")

    # Check for menu items
    menu_items = page.locator(".wp-menu-name").all_text_contents()
    print(f"Menu items found: {len(menu_items)}")
    if menu_items:
        print(f"First few menus: {menu_items[:5]}")

    context.close()
    browser.close()
