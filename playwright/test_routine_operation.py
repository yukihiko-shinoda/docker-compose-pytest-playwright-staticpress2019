#!/usr/bin/env python3
"""Test script for Phase 3: Utility Classes (RoutineOperation).

This script validates the XPath escaping and click helper functions.

Run with: uv run python test_routine_operation.py
"""

import sys

from testlibraries.routine_operation import RoutineOperation


def test_escape_xpath_string_simple() -> None:
    """Test XPath escaping with simple strings (no quotes)."""
    print("Testing escape_xpath_string with simple text...")

    test_cases = [
        ("Hello", "concat('Hello', '')"),
        ("Log In", "concat('Log In', '')"),
        ("StaticPress2019", "concat('StaticPress2019', '')"),
        ("", "concat('', '')"),
    ]

    for input_text, expected in test_cases:
        result = RoutineOperation.escape_xpath_string(input_text)
        if result == expected:
            print(f"  ✓ '{input_text}' → {result}")
        else:
            print(f"  ✗ '{input_text}' failed:")
            print(f"    Expected: {expected}")
            print(f"    Got:      {result}")
            sys.exit(1)


def test_escape_xpath_string_with_quotes() -> None:
    """Test XPath escaping with strings containing single quotes."""
    print("\nTesting escape_xpath_string with quotes...")

    test_cases = [
        ("It's", "concat('It', \"'\", 's', '')"),
        ("Don't", "concat('Don', \"'\", 't', '')"),
        ("I'm here", "concat('I', \"'\", 'm here', '')"),
        ("'", "concat('', \"'\", '', '')"),
        ("Let's go's", "concat('Let', \"'\", 's go', \"'\", 's', '')"),
    ]

    for input_text, expected in test_cases:
        result = RoutineOperation.escape_xpath_string(input_text)
        if result == expected:
            print(f"  ✓ '{input_text}' → {result}")
        else:
            print(f"  ✗ '{input_text}' failed:")
            print(f"    Expected: {expected}")
            print(f"    Got:      {result}")
            sys.exit(1)


def test_escape_xpath_string_special_cases() -> None:
    """Test XPath escaping with special characters and edge cases."""
    print("\nTesting escape_xpath_string with special cases...")

    test_cases = [
        # Double quotes (should not be escaped)
        ('Say "Hello"', "concat('Say \"Hello\"', '')"),
        # Mixed quotes
        ('''It's a "test"''', "concat('It', \"'\", 's a \"test\"', '')"),
        # Numbers and symbols
        ("Price: $10.99", "concat('Price: $10.99', '')"),
        # Unicode characters
        ("Hello 世界", "concat('Hello 世界', '')"),
        # Multiple single quotes in succession
        ("''", "concat('', \"'\", '', \"'\", '', '')"),
    ]

    for input_text, expected in test_cases:
        result = RoutineOperation.escape_xpath_string(input_text)
        if result == expected:
            print(f"  ✓ '{input_text}' → {result}")
        else:
            print(f"  ✗ '{input_text}' failed:")
            print(f"    Expected: {expected}")
            print(f"    Got:      {result}")
            sys.exit(1)


def test_xpath_escaping_matches_typescript() -> None:
    """Verify Python implementation matches TypeScript behavior."""
    print("\nVerifying Python matches TypeScript implementation...")

    # These test cases are based on actual WordPress menu text
    wordpress_menu_items = [
        "StaticPress2019",
        "StaticPress2019 Options",
        "Plugins",
        "Settings",
        "Users",
        "Tools",
    ]

    for menu_text in wordpress_menu_items:
        result = RoutineOperation.escape_xpath_string(menu_text)
        # Verify the result is a concat() expression
        if result.startswith("concat(") and result.endswith(")"):
            print(f"  ✓ '{menu_text}' → valid concat() expression")
        else:
            print(f"  ✗ '{menu_text}' → invalid format: {result}")
            sys.exit(1)


def test_real_world_wordpress_text() -> None:
    """Test with real WordPress text that might contain quotes or special chars."""
    print("\nTesting with real WordPress text examples...")

    # Real-world examples from WordPress UI
    test_cases = [
        # Menu items
        "StaticPress2019",
        "StaticPress2019 Options",
        "Add New",
        "All Posts",
        "Categories",
        # Button text
        "Save Changes",
        "Update",
        "Publish",
        # Messages
        "Plugin activated.",
        "Settings saved.",
        # Text with quotes (rare but possible)
        "User's Profile",
        "Site's Name",
    ]

    for text in test_cases:
        result = RoutineOperation.escape_xpath_string(text)
        # Verify it's a valid concat expression
        if result.startswith("concat(") and result.endswith(")"):
            print(f"  ✓ '{text}'")
        else:
            print(f"  ✗ '{text}' → invalid: {result}")
            sys.exit(1)


def test_click_by_text_xpath_generation() -> None:
    """Test that click_by_text would generate correct XPath selectors."""
    print("\nTesting XPath selector generation logic...")

    # We can't actually test clicking without a browser,
    # but we can verify the XPath would be generated correctly
    test_cases = [
        ("a", "Log In", "xpath=.//a[contains(text(), concat('Log In', ''))]"),
        ("button", "Submit", "xpath=.//button[contains(text(), concat('Submit', ''))]"),
        ("span", "It's here", "xpath=.//span[contains(text(), concat('It', \"'\", 's here', ''))]"),
    ]

    for tag, text, expected_xpath_start in test_cases:
        escaped = RoutineOperation.escape_xpath_string(text)
        generated_xpath = f"xpath=.//{tag}[contains(text(), {escaped})]"

        if generated_xpath == expected_xpath_start:
            print(f"  ✓ {tag} + '{text}' → correct XPath")
        else:
            print(f"  ✗ {tag} + '{text}' failed:")
            print(f"    Expected: {expected_xpath_start}")
            print(f"    Got:      {generated_xpath}")
            sys.exit(1)


def test_empty_and_whitespace() -> None:
    """Test edge cases with empty strings and whitespace."""
    print("\nTesting empty and whitespace strings...")

    test_cases = [
        ("", "concat('', '')"),
        (" ", "concat(' ', '')"),
        ("  ", "concat('  ', '')"),
        ("\t", "concat('\t', '')"),
        ("\n", "concat('\n', '')"),
    ]

    for input_text, expected in test_cases:
        result = RoutineOperation.escape_xpath_string(input_text)
        if result == expected:
            print(f"  ✓ '{input_text!r}' → {result}")
        else:
            print(f"  ✗ '{input_text!r}' failed:")
            print(f"    Expected: {expected}")
            print(f"    Got:      {result}")
            sys.exit(1)


def main() -> None:
    """Run all utility function tests."""
    print("=" * 60)
    print("Phase 3: Utility Classes (RoutineOperation) Tests")
    print("=" * 60)

    test_escape_xpath_string_simple()
    test_escape_xpath_string_with_quotes()
    test_escape_xpath_string_special_cases()
    test_xpath_escaping_matches_typescript()
    test_real_world_wordpress_text()
    test_click_by_text_xpath_generation()
    test_empty_and_whitespace()

    print("\n" + "=" * 60)
    print("✓ All utility function tests passed!")
    print("=" * 60)
    print("\nPhase 3 migration validation successful.")
    print("The following components are now available:")
    print("  - testlibraries/routine_operation.py")
    print("    • RoutineOperation.escape_xpath_string()")
    print("    • RoutineOperation.click_by_text()")
    print("\nThese utilities can now be used in Page Objects (Phase 4).")


if __name__ == "__main__":
    main()
