#!/usr/bin/env python3
"""Test script for Phase 4: Page Objects migration.

This script validates that all page object classes are properly defined
and can be instantiated.

Run with: uv run python test_page_objects.py
"""

import sys

# Test imports
print("=" * 60)
print("Phase 4: Page Objects Migration Tests")
print("=" * 60)


def test_imports() -> None:
    """Test that all page objects can be imported."""
    print("\nTesting imports...")

    try:
        from testlibraries.pages import PageAdmin
        from testlibraries.pages import PageLanguageChooser
        from testlibraries.pages import PageLogin
        from testlibraries.pages import PagePlugins
        from testlibraries.pages import PageStaticPress
        from testlibraries.pages import PageStaticPressOptions
        from testlibraries.pages import PageWelcome

        print("  ✓ PageLogin")
        print("  ✓ PageWelcome")
        print("  ✓ PageLanguageChooser")
        print("  ✓ PageAdmin")
        print("  ✓ PagePlugins")
        print("  ✓ PageStaticPressOptions")
        print("  ✓ PageStaticPress")

        # Store for later use
        return {
            "PageAdmin": PageAdmin,
            "PageLanguageChooser": PageLanguageChooser,
            "PageLogin": PageLogin,
            "PagePlugins": PagePlugins,
            "PageStaticPress": PageStaticPress,
            "PageStaticPressOptions": PageStaticPressOptions,
            "PageWelcome": PageWelcome,
        }
    except ImportError as e:
        print(f"  ✗ Import failed: {e}")
        sys.exit(1)


def test_class_structure(page_classes: dict) -> None:
    """Test that page objects have expected structure."""
    print("\nTesting class structure...")

    # Expected methods for each page object
    expected_methods = {
        "PageLogin": ["__init__", "login"],
        "PageWelcome": ["__init__", "install", "is_displayed_now"],
        "PageLanguageChooser": ["__init__", "choose", "is_displayed_now"],
        "PageAdmin": ["__init__", "hover_menu", "click_menu", "wait_for_submenu", "click_submenu"],
        "PagePlugins": ["__init__", "activate_plugin"],
        "PageStaticPressOptions": ["__init__", "set_options"],
        "PageStaticPress": ["__init__", "click_rebuild"],
    }

    for class_name, expected in expected_methods.items():
        cls = page_classes[class_name]
        actual = [method for method in dir(cls) if not method.startswith("__") or method == "__init__"]

        # Check that all expected methods exist
        for method in expected:
            if method == "__init__":
                continue  # Skip __init__ in the check below
            if method not in actual and f"_{method}" not in actual:
                print(f"  ✗ {class_name} missing method: {method}")
                sys.exit(1)

        print(f"  ✓ {class_name} has all expected methods")


def test_instantiation() -> None:
    """Test that page objects can be instantiated (with mock page)."""
    print("\nTesting instantiation (with mock)...")

    from unittest.mock import Mock

    from testlibraries.pages import PageAdmin
    from testlibraries.pages import PageLanguageChooser
    from testlibraries.pages import PageLogin
    from testlibraries.pages import PagePlugins
    from testlibraries.pages import PageStaticPress
    from testlibraries.pages import PageStaticPressOptions
    from testlibraries.pages import PageWelcome

    # Create a mock Page object
    mock_page = Mock()

    try:
        # Instantiate each page object
        PageLogin(mock_page)
        print("  ✓ PageLogin instantiated")

        PageWelcome(mock_page)
        print("  ✓ PageWelcome instantiated")

        PageLanguageChooser(mock_page)
        print("  ✓ PageLanguageChooser instantiated")

        PageAdmin(mock_page)
        print("  ✓ PageAdmin instantiated")

        PagePlugins(mock_page)
        print("  ✓ PagePlugins instantiated")

        PageStaticPressOptions(mock_page)
        print("  ✓ PageStaticPressOptions instantiated")

        PageStaticPress(mock_page)
        print("  ✓ PageStaticPress instantiated")

    except Exception as e:
        print(f"  ✗ Instantiation failed: {e}")
        sys.exit(1)


def test_type_hints() -> None:
    """Test that page objects have proper type hints."""
    print("\nTesting type hints...")

    from testlibraries.pages import PageAdmin
    from testlibraries.pages import PageLanguageChooser
    from testlibraries.pages import PageLogin
    from testlibraries.pages import PagePlugins
    from testlibraries.pages import PageStaticPress
    from testlibraries.pages import PageStaticPressOptions
    from testlibraries.pages import PageWelcome

    # Check __init__ method has type hints
    classes_to_check = [
        PageLogin,
        PageWelcome,
        PageLanguageChooser,
        PageAdmin,
        PagePlugins,
        PageStaticPressOptions,
        PageStaticPress,
    ]

    for cls in classes_to_check:
        # Check that __init__ accepts page parameter
        init_annotations = cls.__init__.__annotations__
        if "page" in init_annotations:
            print(f"  ✓ {cls.__name__}.__init__ has type hint for 'page'")
        else:
            print(f"  ✗ {cls.__name__}.__init__ missing type hint for 'page'")
            sys.exit(1)


def test_routine_operation_integration() -> None:
    """Test that page objects using RoutineOperation imported correctly."""
    print("\nTesting RoutineOperation integration...")

    try:
        # These page objects use RoutineOperation
        # Verify they import RoutineOperation in their module
        import inspect

        from testlibraries.pages.page_admin import PageAdmin
        from testlibraries.pages.page_plugins import PagePlugins

        # Check PageAdmin uses RoutineOperation
        admin_source = inspect.getsource(PageAdmin)
        if "RoutineOperation" in admin_source:
            print("  ✓ PageAdmin uses RoutineOperation")
        else:
            print("  ✗ PageAdmin should use RoutineOperation")
            sys.exit(1)

        # Check PagePlugins uses RoutineOperation
        plugins_source = inspect.getsource(PagePlugins)
        if "RoutineOperation" in plugins_source:
            print("  ✓ PagePlugins uses RoutineOperation")
        else:
            print("  ✗ PagePlugins should use RoutineOperation")
            sys.exit(1)

    except Exception as e:
        print(f"  ✗ RoutineOperation integration test failed: {e}")
        sys.exit(1)


def test_docstrings() -> None:
    """Test that page objects have docstrings."""
    print("\nTesting docstrings...")

    from testlibraries.pages import PageAdmin
    from testlibraries.pages import PageLanguageChooser
    from testlibraries.pages import PageLogin
    from testlibraries.pages import PagePlugins
    from testlibraries.pages import PageStaticPress
    from testlibraries.pages import PageStaticPressOptions
    from testlibraries.pages import PageWelcome

    classes = [
        PageLogin,
        PageWelcome,
        PageLanguageChooser,
        PageAdmin,
        PagePlugins,
        PageStaticPressOptions,
        PageStaticPress,
    ]

    for cls in classes:
        if cls.__doc__:
            print(f"  ✓ {cls.__name__} has class docstring")
        else:
            print(f"  ✗ {cls.__name__} missing class docstring")
            sys.exit(1)


def test_method_signatures() -> None:
    """Test that methods have correct signatures."""
    print("\nTesting method signatures...")

    import inspect

    from testlibraries.pages import PageLogin
    from testlibraries.pages import PageStaticPressOptions

    # Test PageLogin.login signature
    sig = inspect.signature(PageLogin.login)
    params = list(sig.parameters.keys())
    if params == ["self", "user_name", "user_password"]:
        print("  ✓ PageLogin.login has correct signature")
    else:
        print(f"  ✗ PageLogin.login signature mismatch: {params}")
        sys.exit(1)

    # Test PageStaticPressOptions.set_options signature
    sig = inspect.signature(PageStaticPressOptions.set_options)
    params = list(sig.parameters.keys())
    expected = [
        "self",
        "static_url",
        "dump_directory",
        "basic_authentication_user",
        "basic_authentication_password",
        "request_timeout",
    ]
    if params == expected:
        print("  ✓ PageStaticPressOptions.set_options has correct signature")
    else:
        print("  ✗ PageStaticPressOptions.set_options signature mismatch")
        print(f"    Expected: {expected}")
        print(f"    Got: {params}")
        sys.exit(1)


def main() -> None:
    """Run all page object tests."""
    page_classes = test_imports()
    test_class_structure(page_classes)
    test_instantiation()
    test_type_hints()
    test_routine_operation_integration()
    test_docstrings()
    test_method_signatures()

    print("\n" + "=" * 60)
    print("✓ All page object tests passed!")
    print("=" * 60)
    print("\nPhase 4 migration validation successful.")
    print("The following page objects are now available:")
    print("  - testlibraries/pages/page_login.py (PageLogin)")
    print("  - testlibraries/pages/page_welcome.py (PageWelcome)")
    print("  - testlibraries/pages/page_language_chooser.py (PageLanguageChooser)")
    print("  - testlibraries/pages/page_admin.py (PageAdmin)")
    print("  - testlibraries/pages/page_plugins.py (PagePlugins)")
    print("  - testlibraries/pages/page_staticpress_options.py (PageStaticPressOptions)")
    print("  - testlibraries/pages/page_staticpress.py (PageStaticPress)")
    print("\nThese page objects can now be used in Phase 5 (Pytest Configuration).")


if __name__ == "__main__":
    main()
