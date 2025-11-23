#!/usr/bin/env python
"""Check if WordPress needs installation."""

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

    # Navigate to WordPress root
    page.goto(HOST, wait_until="networkidle")

    print(f"URL: {page.url}")
    print(f"Title: {page.title()}")

    # Take screenshot
    page.screenshot(path="check_wp_install.png")

    # Check for welcome/installation page
    info_needed = page.locator('xpath=.//*[self::h1 or self::h2][text()="Information needed"]')
    print(f"\n'Information needed' heading found: {info_needed.count() > 0}")

    # Check for language chooser
    lang_chooser = page.locator('label:has-text("Site Language")')
    print(f"Language chooser found: {lang_chooser.count() > 0}")

    # Check if already installed (login page or admin)
    login_form = page.locator("input#user_login")
    print(f"Login form found: {login_form.count() > 0}")

    context.close()
    browser.close()
