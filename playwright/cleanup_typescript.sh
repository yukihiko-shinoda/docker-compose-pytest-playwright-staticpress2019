#!/bin/bash
#
# Phase 8: Cleanup Script - Remove TypeScript files and artifacts
#
# This script removes all TypeScript files, configurations, and npm artifacts
# after the successful migration to Python.
#
# Usage: bash cleanup_typescript.sh
#

set -e  # Exit on error

echo "=============================================="
echo "Phase 8: TypeScript to Python Migration Cleanup"
echo "=============================================="
echo ""

# Confirmation prompt
read -p "This will delete all TypeScript files and npm artifacts. Continue? (y/N) " -n 1 -r
echo
if [[ ! $REPLY =~ ^[Yy]$ ]]
then
    echo "Cleanup cancelled."
    exit 1
fi

echo ""
echo "Step 1: Removing TypeScript test directory..."
if [ -d "__tests__" ]; then
    rm -rf __tests__
    echo "✓ Removed __tests__/"
else
    echo "  (already removed)"
fi

echo ""
echo "Step 2: Removing TypeScript source files..."
files_to_remove=(
    "testlibraries/FixtureLoader.ts"
    "testlibraries/RoutineOperation.ts"
    "testlibraries/TableCleaner.ts"
)

for file in "${files_to_remove[@]}"; do
    if [ -f "$file" ]; then
        rm "$file"
        echo "✓ Removed $file"
    fi
done

echo ""
echo "Step 3: Removing TypeScript entity files..."
if [ -d "testlibraries/entities" ]; then
    find testlibraries/entities -name "*.ts" -type f -delete
    echo "✓ Removed all .ts files from testlibraries/entities/"
    # Check if directory is empty (except __init__.py)
    file_count=$(find testlibraries/entities -type f ! -name "__init__.py" | wc -l)
    if [ "$file_count" -eq 0 ]; then
        echo "  Entity directory now contains only Python files"
    fi
else
    echo "  (already removed)"
fi

echo ""
echo "Step 4: Removing TypeScript page object files..."
if [ -d "testlibraries/pages" ]; then
    find testlibraries/pages -name "*.ts" -type f -delete
    echo "✓ Removed all .ts files from testlibraries/pages/"
    # Check if directory is empty (except __init__.py)
    file_count=$(find testlibraries/pages -type f ! -name "__init__.py" ! -name "*.py" | wc -l)
    if [ "$file_count" -eq 0 ]; then
        echo "  Pages directory now contains only Python files"
    fi
else
    echo "  (already removed)"
fi

echo ""
echo "Step 5: Removing TypeScript configuration files..."
config_files=(
    "tsconfig.json"
    "playwright.config.ts"
    "ormconfig.ts"
)

for file in "${config_files[@]}"; do
    if [ -f "$file" ]; then
        rm "$file"
        echo "✓ Removed $file"
    fi
done

echo ""
echo "Step 6: Removing Jest configuration files..."
jest_files=(
    "jest.config.js"
    "jest-puppeteer.config.js"
)

for file in "${jest_files[@]}"; do
    if [ -f "$file" ]; then
        rm "$file"
        echo "✓ Removed $file"
    fi
done

echo ""
echo "Step 7: Removing JavaScript mock files..."
if [ -f "testlibraries/mocks/faker.js" ]; then
    rm testlibraries/mocks/faker.js
    echo "✓ Removed testlibraries/mocks/faker.js"
    # Remove mocks directory if empty
    if [ -d "testlibraries/mocks" ] && [ -z "$(ls -A testlibraries/mocks)" ]; then
        rmdir testlibraries/mocks
        echo "✓ Removed empty testlibraries/mocks/ directory"
    fi
fi

echo ""
echo "Step 8: Removing npm artifacts..."
if [ -d "node_modules" ]; then
    rm -rf node_modules
    echo "✓ Removed node_modules/"
else
    echo "  node_modules/ (already removed)"
fi

if [ -f "package.json" ]; then
    rm package.json
    echo "✓ Removed package.json"
fi

if [ -f "package-lock.json" ]; then
    rm package-lock.json
    echo "✓ Removed package-lock.json"
fi

echo ""
echo "Step 9: Verifying cleanup..."
echo ""

# Check for remaining TypeScript files
ts_count=$(find . -name "*.ts" ! -path "./node_modules/*" ! -path "./.venv/*" 2>/dev/null | wc -l)
echo "  Remaining .ts files: $ts_count"

if [ "$ts_count" -eq 0 ]; then
    echo "  ✓ All TypeScript files removed successfully!"
else
    echo "  ⚠ Warning: Some TypeScript files remain:"
    find . -name "*.ts" ! -path "./node_modules/*" ! -path "./.venv/*" 2>/dev/null
fi

# Check for remaining JavaScript config files
js_count=$(find . -maxdepth 1 -name "*.js" 2>/dev/null | wc -l)
echo "  Remaining .js config files in root: $js_count"

if [ "$js_count" -eq 0 ]; then
    echo "  ✓ All JavaScript config files removed!"
fi

echo ""
echo "=============================================="
echo "Cleanup Complete!"
echo "=============================================="
echo ""
echo "Next steps:"
echo "1. Verify Python tests still work: uv run pytest -v"
echo "2. Check git status: git status"
echo "3. Commit the changes: git add -A && git commit -m 'Complete Phase 8: Remove TypeScript files'"
echo ""
echo "The project has been successfully migrated to Python!"
