#!/usr/bin/env python3
"""Test script for Phase 6: Main Test File validation.

This script validates that tests/test_all.py is properly structured and can be
imported without errors.

Run with: uv run python test_phase6_main_test.py
"""

import sys


def test_test_all_imports() -> None:
    """Test that tests/test_all.py can be imported."""
    print("Testing tests/test_all.py imports...")

    try:
        import tests.test_all  # noqa: F401

        print("  ✓ tests/test_all.py imported successfully")
    except ImportError as e:
        print(f"  ✗ Failed to import tests/test_all.py: {e}")
        sys.exit(1)
    except Exception as e:
        print(f"  ✗ Error importing tests/test_all.py: {e}")
        sys.exit(1)


def test_constants_defined() -> None:
    """Test that configuration constants are defined."""
    print("\nTesting configuration constants...")

    import tests.test_all as test_module

    required_constants = [
        "HOST",
        "BASIC_AUTH_USERNAME",
        "BASIC_AUTH_PASSWORD",
        "USERNAME",
        "PASSWORD",
    ]

    for const in required_constants:
        if hasattr(test_module, const):
            value = getattr(test_module, const)
            print(f"  ✓ {const} = {value!r}")
        else:
            print(f"  ✗ {const} is not defined")
            sys.exit(1)


def test_test_function_defined() -> None:
    """Test that test function is defined."""
    print("\nTesting test function...")

    import tests.test_all as test_module

    test_function = "test_sets_option_and_rebuilds"

    if hasattr(test_module, test_function):
        func = getattr(test_module, test_function)
        if callable(func):
            print(f"  ✓ {test_function} function defined")
        else:
            print(f"  ✗ {test_function} is not callable")
            sys.exit(1)
    else:
        print(f"  ✗ {test_function} function not found")
        sys.exit(1)


def test_imports_required_modules() -> None:
    """Test that test_all.py imports all required modules."""
    print("\nTesting required imports...")

    import inspect

    import tests.test_all as test_module

    source = inspect.getsource(test_module)

    required_imports = [
        "Page",
        "expect",
        "text",
        "get_db_connection",
        "PageAdmin",
        "PageLogin",
        "PageStaticPress",
        "PageStaticPressOptions",
    ]

    for import_name in required_imports:
        if import_name in source:
            print(f"  ✓ {import_name} imported")
        else:
            print(f"  ✗ {import_name} not found in imports")
            sys.exit(1)


def test_function_signature() -> None:
    """Test that test function has correct signature."""
    print("\nTesting function signature...")

    import inspect

    import tests.test_all as test_module

    func = test_module.test_sets_option_and_rebuilds
    sig = inspect.signature(func)
    params = list(sig.parameters.keys())

    if params == ["page"]:
        print("  ✓ test_sets_option_and_rebuilds has correct signature: (page)")
    else:
        print(f"  ✗ test_sets_option_and_rebuilds signature mismatch: {params}")
        sys.exit(1)


def test_function_has_docstring() -> None:
    """Test that test function has proper documentation."""
    print("\nTesting docstring...")

    import tests.test_all as test_module

    func = test_module.test_sets_option_and_rebuilds

    if func.__doc__:
        print("  ✓ test_sets_option_and_rebuilds has docstring")
        # Check for key content
        if "database" in func.__doc__.lower():
            print("  ✓ Docstring mentions database validation")
        if "rebuild" in func.__doc__.lower():
            print("  ✓ Docstring mentions rebuild functionality")
    else:
        print("  ✗ test_sets_option_and_rebuilds missing docstring")
        sys.exit(1)


def test_references_typescript() -> None:
    """Test that test file references the original TypeScript code."""
    print("\nTesting TypeScript references...")

    import inspect

    import tests.test_all as test_module

    source = inspect.getsource(test_module)

    if "all.test.ts" in source:
        print("  ✓ References TypeScript test file")
    else:
        print("  ⚠ No explicit reference to TypeScript test file")

    if "lines" in source and ("99" in source or "152" in source):
        print("  ✓ References specific TypeScript line numbers")
    else:
        print("  ⚠ No explicit line number references")


def test_test_structure() -> None:
    """Test that test follows proper structure."""
    print("\nTesting test structure...")

    import inspect

    import tests.test_all as test_module

    source = inspect.getsource(test_module.test_sets_option_and_rebuilds)

    # Check for key steps
    steps = {
        "login": ["PageLogin", "login"],
        "navigation": ["PageAdmin", "hover_menu"],
        "set options": ["PageStaticPressOptions", "set_options"],
        "database verification": ["get_db_connection", "assert"],
        "rebuild": ["PageStaticPress", "click_rebuild"],
        "assertion": ["expect", "to_be_visible"],
    }

    for step_name, keywords in steps.items():
        if all(keyword in source for keyword in keywords):
            print(f"  ✓ Test includes {step_name} step")
        else:
            print(f"  ✗ Test missing {step_name} step")
            sys.exit(1)


def test_database_assertions() -> None:
    """Test that database assertions are present."""
    print("\nTesting database assertions...")

    import inspect

    import tests.test_all as test_module

    source = inspect.getsource(test_module.test_sets_option_and_rebuilds)

    # Check for all three database assertions
    assertions = [
        "StaticPress::static url",
        "StaticPress::static dir",
        "StaticPress::timeout",
    ]

    for assertion in assertions:
        if assertion in source:
            print(f"  ✓ Validates {assertion} in database")
        else:
            print(f"  ✗ Missing validation for {assertion}")
            sys.exit(1)


def test_playwright_assertions() -> None:
    """Test that Playwright assertions are present."""
    print("\nTesting Playwright assertions...")

    import inspect

    import tests.test_all as test_module

    source = inspect.getsource(test_module.test_sets_option_and_rebuilds)

    # Check for Playwright expect assertion
    if "expect" in source and "to_be_visible" in source:
        print("  ✓ Uses Playwright expect().to_be_visible() assertion")
    else:
        print("  ✗ Missing Playwright assertion")
        sys.exit(1)

    # Check for output file validation (may be in regex pattern)
    if "/tmp/static/sub/index" in source or "tmp/static/sub/index" in source:
        print("  ✓ Validates expected output file path")
    else:
        print("  ✗ Missing output file validation")
        sys.exit(1)


def test_pytest_compatibility() -> None:
    """Test that test is compatible with pytest."""
    print("\nTesting pytest compatibility...")

    import tests.test_all as test_module

    func = test_module.test_sets_option_and_rebuilds

    # Check function name starts with test_
    if func.__name__.startswith("test_"):
        print("  ✓ Function name follows pytest convention (test_*)")
    else:
        print("  ✗ Function name doesn't follow pytest convention")
        sys.exit(1)

    # Check function is in tests/ directory
    if "tests" in test_module.__file__:
        print("  ✓ Test file is in tests/ directory")
    else:
        print("  ✗ Test file not in tests/ directory")
        sys.exit(1)


def main() -> None:
    """Run all Phase 6 main test validation tests."""
    print("=" * 60)
    print("Phase 6: Main Test File Tests")
    print("=" * 60)

    test_test_all_imports()
    test_constants_defined()
    test_test_function_defined()
    test_imports_required_modules()
    test_function_signature()
    test_function_has_docstring()
    test_references_typescript()
    test_test_structure()
    test_database_assertions()
    test_playwright_assertions()
    test_pytest_compatibility()

    print("\n" + "=" * 60)
    print("✓ All Phase 6 main test validation tests passed!")
    print("=" * 60)
    print("\nPhase 6 migration validation successful.")
    print("The following components are now available:")
    print("  - tests/test_all.py")
    print("    • test_sets_option_and_rebuilds()")
    print("      - Logs into WordPress")
    print("      - Sets StaticPress options")
    print("      - Verifies options in database")
    print("      - Triggers rebuild")
    print("      - Validates rebuild output")
    print("\nThe test is ready to run (requires WordPress and database):")
    print("  uv run pytest tests/test_all.py -v")
    print("\nAll phases of the TypeScript to Python migration are now complete!")


if __name__ == "__main__":
    main()
