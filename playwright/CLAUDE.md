# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

This is an E2E integration test suite for **StaticPress** (a WordPress plugin) using **Playwright** and **Python**. The tests verify WordPress installation, plugin activation, configuration, and the rebuild functionality of StaticPress2019.

**Technology Stack:**
- Python 3.10+
- uv (package manager)
- pytest (testing framework)
- pytest-playwright (Playwright integration)
- SQLAlchemy 2.0 (ORM)
- PyMySQL (MySQL driver)

## Commands

### Running Tests
```bash
uv run pytest                      # Run all E2E tests
uv run pytest --headed             # Run tests in headed mode (see browser)
uv run pytest -v                   # Run with verbose output
uv run pytest -k "pattern"         # Run tests matching pattern
uv run pytest --html=report.html   # Generate HTML report
```

### Development Setup
```bash
uv sync                                    # Install dependencies from pyproject.toml
uv run playwright install chromium         # Install Playwright browsers
uv run playwright install --with-deps chromium  # Install with system dependencies
```

### Environment Configuration
The project uses `.env` files for configuration. Key environment variables:
- `HOST` - WordPress site URL (default: http://localhost/)
- `DATABASE_HOST` - MySQL host (default: localhost)
- `HEADLESS` - Run browser in headless mode (default: true)

## Architecture

### Test Structure
- **Main test file**: `tests/test_all.py` - Contains the primary E2E test flow
- **Page Object Model**: `testlibraries/pages/` - Separate page objects for each WordPress admin page
- **Test utilities**: `testlibraries/` - Shared helper classes
- **Test configuration**: `conftest.py` - Pytest fixtures and session setup

### Key Components

**Database Integration (SQLAlchemy 2.0)**
- `testlibraries/config.py` - Database configuration with SQLAlchemy connection URL
- `testlibraries/entities/` - SQLAlchemy model definitions for WordPress database tables (wp_options, wp_posts, etc.)
- `testlibraries/fixture_loader.py` - Loads YAML fixtures into the database using raw SQL queries
- `testlibraries/table_cleaner.py` - Cleans up StaticPress-specific options before each test
- Connection pattern: Context manager (`with get_db_connection()`) → Execute operations → Auto-commit/rollback → Auto-close
- Uses parameterized queries with `text()` for SQL injection protection

**Page Objects (Playwright)**
- `page_welcome.py` - WordPress installation flow
- `page_login.py` - Login functionality
- `page_admin.py` - WordPress admin menu navigation (hover, click menu/submenu)
- `page_plugins.py` - Plugin activation
- `page_staticpress_options.py` - StaticPress configuration form
- `page_staticpress.py` - StaticPress rebuild operations
- `page_language_chooser.py` - WordPress 5.4.2+ language selection

**Utility Classes**
- `routine_operation.py` - XPath-based helpers for clicking elements by text
- All page objects receive a `Page` instance via constructor injection
- All class/function names use `snake_case` following Python conventions

### Test Flow
1. **Session Setup** (`conftest.py` - `setup_wordpress` fixture, runs once):
   - Basic authentication setup
   - Navigate to WordPress
   - Handle language selection if needed (WordPress 5.4.2+)
   - Install WordPress or login
   - Activate StaticPress2019 plugin

2. **Before Each Test** (`setup_database_fixtures` fixture, autouse=True):
   - Clean StaticPress options from database
   - Load fixtures from YAML files

3. **Main Test** (`tests/test_all.py`):
   - Navigate admin pages
   - Set StaticPress options
   - Verify options saved to database
   - Trigger rebuild
   - Verify rebuild output

### Configuration Files

**Python Package Management**
- `pyproject.toml` - Project metadata, dependencies, and build configuration
- Uses `uv` for fast dependency resolution and virtual environment management
- All dependencies pinned with minimum versions

**Pytest Setup**
- `pytest.ini` - Pytest configuration with test discovery patterns and timeout settings
- `conftest.py` - Pytest fixtures for browser setup and WordPress initialization
- Test timeout: 5 minutes (300s) configured in pytest.ini
- Browser context configured with HTTP credentials and viewport settings

**Python**
- Requires Python 3.10+
- Type hints used throughout for better IDE support and type checking
- Compatible with mypy for static type analysis
- All code follows PEP 8 style guidelines

**Docker**
- `Dockerfile` - Based on Playwright Python image with Chromium dependencies
- Installs system packages for headless Chromium
- Uses uv for dependency installation
- Installs Playwright browsers with `uv run playwright install --with-deps chromium`
- Runs tests in container with `uv run pytest`

## Development Notes

### WordPress Compatibility
The test suite supports multiple WordPress versions from 4.6 to 6.8+:

**Automatic Version Detection:**
- `_update_database_version()` automatically detects the installed WordPress version
- Sets appropriate `db_version` to prevent upgrade screens (4.6-6.8 supported)
- Defaults to latest db_version (58975) for newer versions

**Version-Specific Handling:**
- Language chooser page only appears in WordPress 5.4.2+
- Password input: `#pass1` (modern WordPress) vs `#pass1-text` (WordPress 4.3)
- Heading tags: `<h2>` (modern) vs `<h1>` (WordPress 4.3)
- Password hashing: Uses `passlib` with phpass algorithm (compatible with all versions)

**Tested Versions:**
- WordPress 4.6.x (legacy)
- WordPress 6.8.3 (latest)

### Database Fixtures
Fixtures are stored in `testlibraries/fixtures/`:
- `WpOptionsDefault.yml` - Default WordPress options
- `WpOptionsStaticPress2019.yml` - StaticPress-specific test data

### Basic Authentication
Tests support sites behind HTTP basic auth:
- Credentials hardcoded: `authuser` / `authpassword`
- Set via `browser_context_args` fixture in `conftest.py`

### Playwright Best Practices Used
- `page.wait_for_load_state('networkidle')` for stable page loads
- Context managers for resource cleanup
- Screenshots for debugging (`screenshot.png`, `screenshot1.png`)
- XPath queries with `page.locator('xpath=...')` for reliable element selection by text content
- Locators instead of element handles for better auto-waiting and retry behavior
- Page object pattern with Page instances passed via constructor
- Pytest fixtures for setup/teardown instead of beforeAll/beforeEach hooks

## SQLAlchemy Usage Pattern

All database operations follow this pattern using context managers:

```python
from sqlalchemy import create_engine, text
from contextlib import contextmanager

@contextmanager
def get_db_connection():
    """Context manager for database connections"""
    engine = create_engine(DATABASE_URL, **ENGINE_OPTIONS)
    connection = engine.connect()
    try:
        yield connection
        connection.commit()
    except Exception:
        connection.rollback()
        raise
    finally:
        connection.close()
        engine.dispose()

# Usage example
with get_db_connection() as conn:
    result = conn.execute(
        text("SELECT option_value FROM wp_options WHERE option_name = :name"),
        {"name": "StaticPress::static url"}
    )
    row = result.fetchone()
```

**Key Features:**
- Context manager ensures proper connection cleanup
- Automatic commit on success, rollback on exception
- Parameterized queries prevent SQL injection
- Engine disposal prevents connection leaks

## Python Conventions

When working with this codebase, follow these Python conventions:

**Naming Conventions:**
- Functions/methods: `snake_case` (e.g., `click_menu()`, `get_link_handler()`)
- Classes: `PascalCase` (e.g., `PageAdmin`, `TableCleaner`)
- Constants: `UPPER_SNAKE_CASE` (e.g., `DATABASE_URL`, `HOST`)
- Private methods: prefix with `_` (e.g., `_get_link_handler_menu()`)

**Type Hints:**
```python
def login(self, username: str, password: str) -> None:
    """Login to WordPress with provided credentials"""
    # Implementation
```

**Docstrings:**
- Use triple quotes for all docstrings
- Keep them concise but descriptive
- Place immediately after function/class definition

**Imports:**
- Standard library imports first
- Third-party imports second
- Local imports last
- Alphabetically sorted within each group
