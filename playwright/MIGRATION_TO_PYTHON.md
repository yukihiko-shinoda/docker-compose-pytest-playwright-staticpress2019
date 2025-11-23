# Migration Plan: TypeScript to Python

This document outlines the complete migration plan for converting the StaticPress E2E integration test suite from TypeScript to Python.

## Table of Contents

- [Technology Stack Comparison](#technology-stack-comparison)
- [Python ORM Recommendation](#python-orm-recommendation-sqlalchemy-20)
- [Proposed Project Structure](#proposed-project-structure)
- [Key Configuration Files](#key-configuration-files)
- [Migration Mapping Examples](#migration-mapping-examples)
- [Dependencies and Setup](#dependencies-and-setup)
- [Advantages of This Migration](#advantages-of-this-migration)
- [Migration Strategy](#migration-strategy)

---

## Technology Stack Comparison

| Component | Current (TypeScript) | Recommended (Python) |
|-----------|---------------------|---------------------|
| Package Manager | npm | **uv** |
| Test Framework | Playwright Test | **pytest + pytest-playwright** |
| ORM | TypeORM 0.3.x | **SQLAlchemy 2.0.x** |
| Database Driver | mysql (node) | **PyMySQL** or **mysqlclient** |
| Environment Variables | dotenv | **python-dotenv** |
| Type Hints | TypeScript | Python type hints (3.10+) |

---

## Python ORM Recommendation: SQLAlchemy 2.0

### Why SQLAlchemy?

- **Most mature and widely adopted** Python ORM (industry standard)
- **Excellent MySQL support** with multiple driver options
- **Flexible architecture**: Core (SQL toolkit) + ORM (object mapping)
- **Active development**: Version 2.0.44 released October 2025
- **Type safety**: Enhanced type hinting in 2.0
- **Async support**: Native async/await support (optional)
- **Raw SQL support**: Can execute raw queries like your current code does

### Direct TypeORM → SQLAlchemy Mapping

**TypeScript (TypeORM):**
```typescript
import { Column, Entity, Index, PrimaryGeneratedColumn } from "typeorm";

@Index("option_name", ["optionName"], { unique: true })
@Index("autoload", ["autoload"], {})
@Entity("wp_options", { schema: "exampledb" })
export class WpOption {
  @PrimaryGeneratedColumn({ type: "bigint", name: "option_id", unsigned: true })
  optionId!: string;

  @Column("varchar", { name: "option_name", unique: true, length: 191 })
  optionName!: string;

  @Column("longtext", { name: "option_value" })
  optionValue!: string;

  @Column("varchar", { name: "autoload", length: 20, default: () => "'yes'" })
  autoload!: string;
}
```

**Python (SQLAlchemy):**
```python
from sqlalchemy import Column, String, BigInteger, Text, Index
from sqlalchemy.orm import DeclarativeBase

class Base(DeclarativeBase):
    pass

class WpOption(Base):
    __tablename__ = "wp_options"
    __table_args__ = (
        Index('option_name', 'option_name', unique=True),
        Index('autoload', 'autoload'),
        {'schema': 'exampledb'}
    )

    option_id = Column(BigInteger, primary_key=True, autoincrement=True)
    option_name = Column(String(191), unique=True, nullable=False)
    option_value = Column(Text, nullable=False)
    autoload = Column(String(20), default="yes", nullable=False)
```

### Raw Query Pattern (Matching Current Approach)

Your current code avoids loading entities with decorators and uses raw queries. SQLAlchemy supports this pattern excellently:

**TypeScript (Current):**
```typescript
import { DataSource } from "typeorm";
import ormconfig from "../ormconfig";

let connection;
try {
  const myDataSource = new DataSource(ormconfig);
  connection = await myDataSource.initialize();

  const result = await connection.query(
    "SELECT option_value FROM wp_options WHERE option_name = 'StaticPress::static url'"
  );
} finally {
  if (connection) {
    await connection.destroy();
  }
}
```

**Python (Proposed):**
```python
from sqlalchemy import create_engine, text
from contextlib import contextmanager

@contextmanager
def get_db_connection():
    engine = create_engine(DATABASE_URL)
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

# Usage
with get_db_connection() as conn:
    result = conn.execute(
        text("SELECT option_value FROM wp_options WHERE option_name = :name"),
        {"name": "StaticPress::static url"}
    )
    row = result.fetchone()
```

---

## Proposed Project Structure

```
/workspace/
├── pyproject.toml              # uv project config (replaces package.json)
├── .env                        # Environment variables
├── pytest.ini                  # Pytest configuration
├── conftest.py                 # Pytest fixtures and setup
├── MIGRATION_TO_PYTHON.md      # This document
│
├── tests/                      # Test directory (replaces __tests__)
│   ├── __init__.py
│   └── test_all.py            # Main test file (replaces all.test.ts)
│
├── testlibraries/
│   ├── __init__.py
│   │
│   ├── config.py              # Database config (replaces ormconfig.ts)
│   ├── fixture_loader.py      # Replaces FixtureLoader.ts
│   ├── table_cleaner.py       # Replaces TableCleaner.ts
│   ├── routine_operation.py   # Replaces RoutineOperation.ts
│   │
│   ├── entities/              # SQLAlchemy models (optional if using raw queries)
│   │   ├── __init__.py
│   │   ├── wp_option.py       # Replaces WpOption.ts
│   │   ├── wp_post.py         # Replaces WpPost.ts
│   │   ├── wp_user.py         # Replaces WpUser.ts
│   │   ├── wp_comment.py      # Replaces WpComment.ts
│   │   ├── wp_term.py         # Replaces WpTerm.ts
│   │   └── ... (other models as needed)
│   │
│   ├── pages/                 # Page Object Model
│   │   ├── __init__.py
│   │   ├── page_welcome.py           # Replaces PageWelcome.ts
│   │   ├── page_login.py             # Replaces PageLogin.ts
│   │   ├── page_admin.py             # Replaces PageAdmin.ts
│   │   ├── page_plugins.py           # Replaces PagePlugins.ts
│   │   ├── page_staticpress_options.py  # Replaces PageStaticPressOptions.ts
│   │   ├── page_staticpress.py       # Replaces PageStaticPress.ts
│   │   └── page_language_chooser.py  # Replaces PageLanguageChooser.ts
│   │
│   └── fixtures/              # YAML fixtures (unchanged)
│       ├── wp_options_default.yml
│       └── wp_options_staticpress2019.yml
│
└── README.md
```

---

## Key Configuration Files

### 1. pyproject.toml (replaces package.json)

```toml
[project]
name = "staticpress-integration-test"
version = "1.0.0"
description = "Integration test for StaticPress"
authors = [{name = "Yukihiko Shinoda"}]
license = {text = "MIT"}
readme = "README.md"
requires-python = ">=3.10"
keywords = ["test", "playwright", "staticpress"]

dependencies = [
    "playwright>=1.56.0",
    "pytest>=8.0.0",
    "pytest-playwright>=0.7.0",
    "sqlalchemy>=2.0.0",
    "pymysql>=1.1.0",
    "python-dotenv>=1.0.0",
    "pyyaml>=6.0",
]

[project.urls]
Repository = "staticpress-integration-test"

[tool.uv]
dev-dependencies = [
    "pytest-html>=4.0.0",
    "mypy>=1.0.0",
]

[tool.pytest.ini_options]
testpaths = ["tests"]
python_files = "test_*.py"
python_classes = "Test*"
python_functions = "test_*"

[build-system]
requires = ["hatchling"]
build-backend = "hatchling.build"
```

### 2. pytest.ini (replaces playwright.config.ts)

```ini
[pytest]
testpaths = tests
python_files = test_*.py
python_classes = Test*
python_functions = test_*

# Playwright options
addopts =
    -v
    --headed
    --browser chromium
    --screenshot on
    --video on
    --output test-results

# Test timeout (5 minutes like the TypeScript version)
timeout = 300

# Markers for organizing tests
markers =
    slow: marks tests as slow (deselect with '-m "not slow"')
    integration: marks tests as integration tests
```

### 3. conftest.py (Pytest fixtures - replaces beforeAll/beforeEach)

```python
"""
Pytest configuration and fixtures for Playwright tests.
This replaces the beforeAll and beforeEach hooks from the TypeScript version.
"""
import pytest
from playwright.sync_api import Page, Browser, BrowserContext
from dotenv import load_dotenv
import os
from testlibraries.fixture_loader import FixtureLoader
from testlibraries.table_cleaner import TableCleaner
from testlibraries.pages.page_welcome import PageWelcome
from testlibraries.pages.page_login import PageLogin
from testlibraries.pages.page_admin import PageAdmin
from testlibraries.pages.page_plugins import PagePlugins
from testlibraries.pages.page_language_chooser import PageLanguageChooser
from testlibraries.routine_operation import RoutineOperation

# Load environment variables
load_dotenv()

# Test configuration
HOST = os.getenv("HOST", "http://localhost/")
USERNAME = "test_user"
PASSWORD = "-JfG+L.3-s!A6YmhsKGkGERc+hq&XswU"


@pytest.fixture(scope="session")
def browser_context_args(browser_context_args):
    """
    Configure browser context with HTTP credentials and viewport.
    This replaces the httpCredentials and viewport settings from playwright.config.ts
    """
    return {
        **browser_context_args,
        "base_url": HOST,
        "http_credentials": {
            "username": "authuser",
            "password": "authpassword"
        },
        "viewport": {"width": 1920, "height": 1080},
        "record_video_dir": "test-results/videos",
        "record_video_size": {"width": 1920, "height": 1080},
    }


@pytest.fixture(scope="session")
def browser_type_launch_args(browser_type_launch_args):
    """
    Configure browser launch options.
    This replaces the launchOptions from playwright.config.ts
    """
    headless = os.getenv("HEADLESS", "true").lower() == "true"
    return {
        **browser_type_launch_args,
        "args": ["--no-sandbox", "--disable-setuid-sandbox"],
        "headless": headless,
    }


@pytest.fixture(scope="session", autouse=True)
def setup_wordpress(browser: Browser):
    """
    One-time setup: Initialize WordPress or login.
    This replaces the test.beforeAll hook from the TypeScript version.
    """
    context = browser.new_context()
    page = context.new_page()

    try:
        print("Start basic authentication")
        page.goto(HOST)
        print("Finish basic authentication")
        page.screenshot(path="screenshot1.png")

        # Handle language chooser (WordPress 5.4.2+)
        page_language_chooser = PageLanguageChooser(page)
        if page_language_chooser.is_displayed_now():
            print("Start choose language")
            page_language_chooser.choose("English (United States)")
            print("Finish choose language")

        # Check if WordPress needs installation or login
        page_welcome = PageWelcome(page)
        if page_welcome.is_displayed_now():
            print("Start Initialize")
            _initialize_wordpress(page)
            print("Finish Initialize")
        else:
            print("Start login")
            _login_wordpress(page)
            print("Finish login")
    finally:
        context.close()


def _initialize_wordpress(page: Page):
    """Initialize WordPress installation"""
    page_welcome = PageWelcome(page)
    page_welcome.install("test_title", USERNAME, PASSWORD, "test@gmail.com")

    RoutineOperation.click_by_text(page, 'a', 'Log In')
    page.wait_for_load_state('networkidle')

    _login_wordpress(page)

    page_admin = PageAdmin(page)
    page_admin.click_menu('Plugins')

    page_plugins = PagePlugins(page)
    page_plugins.activate_plugin('StaticPress2019')


def _login_wordpress(page: Page):
    """Login to WordPress"""
    page.goto(HOST + 'wp-admin/', wait_until='networkidle')
    page_login = PageLogin(page)
    page_login.login(USERNAME, PASSWORD)


@pytest.fixture(autouse=True)
def setup_database_fixtures():
    """
    Setup database fixtures before each test.
    This replaces the test.beforeEach hook from the TypeScript version.
    """
    print("Inserting fixtures into the database...")
    TableCleaner.clean()
    FixtureLoader.load('./testlibraries/fixtures/wp_options_staticpress2019.yml')
    print("Inserted fixtures into the database.")
    yield
    # Cleanup after test if needed
```

### 4. testlibraries/config.py (replaces ormconfig.ts)

```python
"""
Database configuration for SQLAlchemy.
This replaces ormconfig.ts from the TypeScript version.
"""
import os
from dotenv import load_dotenv

load_dotenv()

# Database connection parameters
DATABASE_CONFIG = {
    "host": os.getenv("DATABASE_HOST", "localhost"),
    "port": 3306,
    "username": "exampleuser",
    "password": "examplepass",
    "database": "exampledb",
}

# SQLAlchemy connection URL
DATABASE_URL = (
    f"mysql+pymysql://{DATABASE_CONFIG['username']}:{DATABASE_CONFIG['password']}"
    f"@{DATABASE_CONFIG['host']}:{DATABASE_CONFIG['port']}/{DATABASE_CONFIG['database']}"
)

# SQLAlchemy engine options
ENGINE_OPTIONS = {
    "echo": False,  # Set to True for SQL logging
    "pool_pre_ping": True,  # Verify connections before using
    "pool_recycle": 3600,  # Recycle connections after 1 hour
}
```

---

## Migration Mapping Examples

### Database Connection Pattern

**TypeScript (Current):**
```typescript
import { DataSource } from "typeorm";
import ormconfig from "../ormconfig";

export default class TableCleaner {
  public static async clean() {
    let connection;
    try {
      const myDataSource = new DataSource(ormconfig);
      connection = await myDataSource.initialize();

      await connection.query("DELETE FROM wp_options WHERE option_name = 'StaticPress::static url'");
      await connection.query("DELETE FROM wp_options WHERE option_name = 'StaticPress::static dir'");
      await connection.query("DELETE FROM wp_options WHERE option_name = 'StaticPress::timeout'");
    } catch (err) {
      throw err;
    } finally {
      if (connection) {
        await connection.destroy();
      }
    }
  };
}
```

**Python (Proposed):**
```python
from sqlalchemy import create_engine, text
from contextlib import contextmanager
from .config import DATABASE_URL, ENGINE_OPTIONS

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


class TableCleaner:
    @staticmethod
    def clean():
        """Clean StaticPress options from database"""
        with get_db_connection() as conn:
            conn.execute(text("DELETE FROM wp_options WHERE option_name = 'StaticPress::static url'"))
            conn.execute(text("DELETE FROM wp_options WHERE option_name = 'StaticPress::static dir'"))
            conn.execute(text("DELETE FROM wp_options WHERE option_name = 'StaticPress::timeout'"))
```

### Fixture Loader Pattern

**TypeScript (Current):**
```typescript
export default class FixtureLoader {
  public static async load(fixturesPath: string) {
    let connection;
    try {
      const myDataSource = new DataSource(ormconfig);
      connection = await myDataSource.initialize();

      if (fixturesPath.includes('WpOptionsStaticPress2019')) {
        await connection.query(`
          INSERT INTO wp_options (option_name, option_value, autoload)
          VALUES ('StaticPress::static url', 'http://example.org/sub/', 'yes')
          ON DUPLICATE KEY UPDATE option_value = VALUES(option_value), autoload = VALUES(autoload)
        `);
        // ... more queries
      }
    } finally {
      if (connection) {
        await connection.destroy();
      }
    }
  };
}
```

**Python (Proposed):**
```python
from .config import get_db_connection
from sqlalchemy import text

class FixtureLoader:
    @staticmethod
    def load(fixtures_path: str):
        """Load fixtures into database"""
        with get_db_connection() as conn:
            if 'wp_options_staticpress2019' in fixtures_path.lower():
                conn.execute(text("""
                    INSERT INTO wp_options (option_name, option_value, autoload)
                    VALUES (:name, :value, :autoload)
                    ON DUPLICATE KEY UPDATE
                        option_value = VALUES(option_value),
                        autoload = VALUES(autoload)
                """), {
                    "name": "StaticPress::static url",
                    "value": "http://example.org/sub/",
                    "autoload": "yes"
                })
                # ... more queries
```

### Page Object Pattern

**TypeScript (Current):**
```typescript
import { Page, Locator } from "@playwright/test";
import RoutineOperation from "../RoutineOperation";

export default class PageAdmin {
  constructor(private page: Page) {}

  public async hoverMenu(menu: string): Promise<void> {
    const linkHandlerMenu = this.getLinkHandlerMenu(menu);
    await linkHandlerMenu.hover();
  }

  public async clickMenu(menu: string): Promise<void> {
    const linkHandler = this.getLinkHandlerMenu(menu);
    await linkHandler.click();
    await this.page.waitForLoadState('networkidle');
  }

  public async waitForSubMenu(subMenu: string): Promise<void> {
    const linkHandler = this.getLinkHandlerSubMenu(subMenu);
    await linkHandler.waitFor({ state: 'visible' });
  }

  public async clickSubMenu(subMenu: string): Promise<void> {
    const linkHandler = this.getLinkHandlerSubMenu(subMenu);
    await linkHandler.click();
    await this.page.waitForLoadState('networkidle');
  }

  private getLinkHandlerMenu(menu: string): Locator {
    const escapedMenu = RoutineOperation.escapeXpathString(menu);
    return this.getLinkHandler(`//div[@class="wp-menu-name" and contains(text(), ${escapedMenu})]`);
  }

  private getLinkHandlerSubMenu(subMenu: string): Locator {
    const escapedSubMenu = RoutineOperation.escapeXpathString(subMenu);
    return this.getLinkHandler(`//a[text()=${escapedSubMenu}]`);
  }

  private getLinkHandler(xpath: string): Locator {
    return this.page.locator(`xpath=.${xpath}`).first();
  }
}
```

**Python (Proposed):**
```python
from playwright.sync_api import Page, Locator
from ..routine_operation import RoutineOperation

class PageAdmin:
    def __init__(self, page: Page):
        self.page = page

    def hover_menu(self, menu: str) -> None:
        """Hover over a menu item"""
        link_handler = self._get_link_handler_menu(menu)
        link_handler.hover()

    def click_menu(self, menu: str) -> None:
        """Click on a menu item"""
        link_handler = self._get_link_handler_menu(menu)
        link_handler.click()
        self.page.wait_for_load_state('networkidle')

    def wait_for_submenu(self, submenu: str) -> None:
        """Wait for a submenu to be visible"""
        link_handler = self._get_link_handler_submenu(submenu)
        link_handler.wait_for(state='visible')

    def click_submenu(self, submenu: str) -> None:
        """Click on a submenu item"""
        link_handler = self._get_link_handler_submenu(submenu)
        link_handler.click()
        self.page.wait_for_load_state('networkidle')

    def _get_link_handler_menu(self, menu: str) -> Locator:
        """Get locator for menu item"""
        escaped_menu = RoutineOperation.escape_xpath_string(menu)
        xpath = f'//div[@class="wp-menu-name" and contains(text(), {escaped_menu})]'
        return self._get_link_handler(xpath)

    def _get_link_handler_submenu(self, submenu: str) -> Locator:
        """Get locator for submenu item"""
        escaped_submenu = RoutineOperation.escape_xpath_string(submenu)
        xpath = f'//a[text()={escaped_submenu}]'
        return self._get_link_handler(xpath)

    def _get_link_handler(self, xpath: str) -> Locator:
        """Get first matching locator for XPath"""
        return self.page.locator(f'xpath=.{xpath}').first
```

### Main Test File

**TypeScript (Current):**
```typescript
test.describe('All', () => {
  test("sets option and rebuilds", async ({ page }) => {
    await page.goto(host + 'wp-admin/', { waitUntil: 'networkidle' });
    const pageLogin = new PageLogin(page);
    await pageLogin.login(userName, userPassword);

    const pageAdmin = new PageAdmin(page);
    await pageAdmin.hoverMenu('StaticPress2019');
    await pageAdmin.waitForSubMenu('StaticPress2019 Options');
    await pageAdmin.clickSubMenu('StaticPress2019 Options');

    // ... test continues
  });
});
```

**Python (Proposed):**
```python
import pytest
from playwright.sync_api import Page, expect
from testlibraries.pages.page_login import PageLogin
from testlibraries.pages.page_admin import PageAdmin
from testlibraries.pages.page_staticpress_options import PageStaticPressOptions
from testlibraries.pages.page_staticpress import PageStaticPress
from testlibraries.config import get_db_connection
from sqlalchemy import text
import os

HOST = os.getenv("HOST", "http://localhost/")
USERNAME = "test_user"
PASSWORD = "-JfG+L.3-s!A6YmhsKGkGERc+hq&XswU"


def test_sets_option_and_rebuilds(page: Page):
    """
    Test that options are set in the database and rebuild works.
    This replaces the "sets option and rebuilds" test from all.test.ts
    """
    # Login
    page.goto(HOST + 'wp-admin/', wait_until='networkidle')
    page_login = PageLogin(page)
    page_login.login(USERNAME, PASSWORD)

    # Navigate to StaticPress Options
    page_admin = PageAdmin(page)
    page_admin.hover_menu('StaticPress2019')
    page_admin.wait_for_submenu('StaticPress2019 Options')
    page_admin.click_submenu('StaticPress2019 Options')

    # Set options
    page_staticpress_options = PageStaticPressOptions(page)
    static_url = 'http://example.com/sub/'
    dump_directory = '/tmp/static/'
    request_timeout = '10'

    page_staticpress_options.set_options(
        static_url,
        dump_directory,
        "authuser",
        "authpassword",
        request_timeout
    )

    # Verify options in database
    with get_db_connection() as conn:
        # Check static URL
        result = conn.execute(
            text("SELECT option_value FROM wp_options WHERE option_name = :name"),
            {"name": "StaticPress::static url"}
        )
        row = result.fetchone()
        assert row[0] == static_url

        # Check dump directory
        result = conn.execute(
            text("SELECT option_value FROM wp_options WHERE option_name = :name"),
            {"name": "StaticPress::static dir"}
        )
        row = result.fetchone()
        assert row[0] == dump_directory

        # Check timeout
        result = conn.execute(
            text("SELECT option_value FROM wp_options WHERE option_name = :name"),
            {"name": "StaticPress::timeout"}
        )
        row = result.fetchone()
        assert row[0] == request_timeout

    # Trigger rebuild
    page_admin.hover_menu('StaticPress2019')
    page_admin.wait_for_submenu('StaticPress2019')
    page_admin.click_submenu('StaticPress2019')

    page_staticpress = PageStaticPress(page)
    page_staticpress.click_rebuild()

    # Verify rebuild output
    expect(page.locator('li', has_text=r'.*/tmp/static/sub/index\.html')).to_be_visible()
```

---

## Dependencies and Setup

### Installation with uv

```bash
# Install uv (if not already installed)
curl -LsSf https://astral.sh/uv/install.sh | sh

# Or on macOS/Linux with Homebrew
brew install uv

# Or on Windows with PowerShell
powershell -c "irm https://astral.sh/uv/install.ps1 | iex"

# Initialize project (creates pyproject.toml)
uv init

# Sync dependencies from pyproject.toml
uv sync

# Install Playwright browsers
uv run playwright install chromium

# Or install with dependencies (system packages)
uv run playwright install --with-deps chromium
```

### Running Tests

```bash
# Run all tests
uv run pytest

# Run tests in headed mode
uv run pytest --headed

# Run specific test file
uv run pytest tests/test_all.py

# Run with verbose output
uv run pytest -v

# Run tests matching a pattern
uv run pytest -k "rebuild"

# Generate HTML report
uv run pytest --html=report.html --self-contained-html
```

### Development Commands

```bash
# Add a new dependency
uv add package-name

# Add a dev dependency
uv add --dev package-name

# Update dependencies
uv sync --upgrade

# Run a command in the virtual environment
uv run python script.py

# Activate the virtual environment
source .venv/bin/activate  # Linux/macOS
.venv\Scripts\activate     # Windows
```

---

## Advantages of This Migration

### 1. **Performance**
- **uv**: 10-100x faster than pip for dependency resolution and installation
- **Python**: Lower memory footprint than Node.js
- **SQLAlchemy**: Highly optimized query execution and connection pooling

### 2. **Ecosystem Maturity**
- **SQLAlchemy**: 15+ years of development, more mature than TypeORM
- **pytest**: Industry standard testing framework with extensive plugin ecosystem
- **Playwright Python**: Official support from Microsoft
- **Better WordPress/MySQL tooling** in Python ecosystem

### 3. **Developer Experience**
- **Simpler syntax**: Less boilerplate than TypeScript decorators
- **Better debugging**: Python's debugging tools (pdb, pytest fixtures)
- **Type safety**: Python type hints + mypy provides similar safety to TypeScript
- **uv**: Built-in virtual environment management, no need for separate tools

### 4. **Maintenance**
- **Fewer dependencies**: Python standard library covers more use cases
- **Better stability**: Python's slow release cycle means fewer breaking changes
- **Active community**: Larger Python testing community than TypeScript testing

### 5. **Testing Features**
- **pytest fixtures**: More powerful and flexible than beforeAll/beforeEach
- **Better parallel testing**: pytest-xdist for parallel execution
- **Rich assertion introspection**: pytest shows detailed failure information
- **Parametrized tests**: Easy to run same test with different inputs

---

## Migration Strategy

### Recommended Migration Order

#### Phase 1: Setup Python Environment (Day 1)
1. Install uv
2. Create `pyproject.toml`
3. Create `pytest.ini`
4. Setup `.env` file (if not exists)
5. Test basic Python + Playwright setup

**Validation**: Run `uv run playwright install` successfully

#### Phase 2: Database Layer (Days 2-3)
1. Create `testlibraries/config.py` (database configuration)
2. Create `testlibraries/table_cleaner.py`
3. Create `testlibraries/fixture_loader.py`
4. Optionally create entity models in `testlibraries/entities/`
5. Test database connection and queries

**Validation**: Run table cleaner and fixture loader standalone

#### Phase 3: Utility Classes (Day 4)
1. Create `testlibraries/routine_operation.py`
2. Port XPath escaping and click helpers
3. Test utility functions

**Validation**: Run utility functions with simple test cases

#### Phase 4: Page Objects (Days 5-8)
Migrate page objects one by one, testing each:

1. `testlibraries/pages/page_login.py` (simplest)
2. `testlibraries/pages/page_welcome.py`
3. `testlibraries/pages/page_language_chooser.py`
4. `testlibraries/pages/page_admin.py` (most complex, used by many)
5. `testlibraries/pages/page_plugins.py`
6. `testlibraries/pages/page_staticpress_options.py`
7. `testlibraries/pages/page_staticpress.py`

**Validation**: Create simple test for each page object as you go

#### Phase 5: Pytest Configuration (Day 9)
1. Create `conftest.py` with fixtures
2. Port `beforeAll` logic to session fixture
3. Port `beforeEach` logic to function fixture
4. Test fixture execution order

**Validation**: Run pytest with empty test to verify fixtures work

#### Phase 6: Main Test File (Day 10)
1. Create `tests/test_all.py`
2. Port the main test: "sets option and rebuilds"
3. Verify all assertions work correctly

**Validation**: Full E2E test passes

#### Phase 7: CI/CD and Documentation (Day 11)
1. Update `Dockerfile` for Python
2. Update `README.md` with Python instructions
3. Update `CLAUDE.md` with new architecture
4. Add GitHub Actions workflow (if exists)

**Validation**: Test runs in Docker container

#### Phase 8: Cleanup (Day 12)
1. Remove TypeScript files
2. Remove `node_modules/`, `package.json`, `package-lock.json`
3. Remove `tsconfig.json`, `playwright.config.ts`
4. Final testing and validation

**Validation**: Clean checkout and test run succeeds

### Parallel Development Strategy

If you want to keep both versions running during migration:

```
/workspace/
├── legacy/                    # Move TypeScript files here
│   ├── package.json
│   ├── __tests__/
│   └── testlibraries/
│
├── pyproject.toml            # New Python project
├── tests/                    # New Python tests
└── testlibraries/            # New Python libraries
```

This allows:
- Running TypeScript tests with `cd legacy && npm test`
- Running Python tests with `uv run pytest`
- Comparing outputs to ensure parity
- Gradual migration without breaking existing setup

### Testing Parity Checklist

After migration, verify:
- [ ] All tests pass with same assertions
- [ ] Database fixtures load correctly
- [ ] Page objects work with same selectors
- [ ] Screenshots/videos are captured
- [ ] Timeout settings match (5 minutes)
- [ ] HTTP basic auth works
- [ ] Environment variables are read correctly
- [ ] Error messages are clear and helpful

---

## Additional Resources

### Documentation
- **uv**: https://docs.astral.sh/uv/
- **SQLAlchemy 2.0**: https://docs.sqlalchemy.org/en/20/
- **pytest**: https://docs.pytest.org/
- **Playwright Python**: https://playwright.dev/python/
- **pytest-playwright**: https://github.com/microsoft/playwright-pytest

### Community
- **SQLAlchemy Discord**: https://discord.gg/sqlalchemy
- **Playwright Discord**: https://discord.gg/playwright
- **Python Testing Discord**: https://discord.gg/python

### Migration Tips
1. **Start small**: Migrate one component at a time
2. **Test early, test often**: Don't wait until everything is ported
3. **Keep TypeScript version**: Use for reference and comparison
4. **Use type hints**: Enable mypy for type checking
5. **Follow Python conventions**: Use snake_case, not camelCase
6. **Leverage Python features**: List comprehensions, context managers, etc.

---

## Questions or Issues?

During migration, if you encounter:
- **Database connection issues**: Check DATABASE_HOST in .env
- **Import errors**: Ensure all `__init__.py` files exist
- **Playwright errors**: Run `uv run playwright install --with-deps`
- **XPath issues**: Python uses f-strings differently than template literals
- **Type errors**: Add type hints and run `mypy tests/`

Remember: The Python version will be cleaner, more maintainable, and faster to develop with!
