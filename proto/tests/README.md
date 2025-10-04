# Tests

Test scripts for verifying the project setup and functionality.

## Available Tests

### `test_structure.py`

Validates the project structure and imports.

**Usage:**

```bash
python tests/test_structure.py
# or from root:
python -m tests.test_structure
```

**What it checks:**

- ✅ All required directories exist
- ✅ All required files are present
- ✅ All modules can be imported
- ✅ Leaderboard configuration (if .env exists)

### `test_setup.py`

Original setup test (legacy).

**Usage:**

```bash
python tests/test_setup.py
```

## Running Tests

From the project root:

```bash
# Run structure validation
python tests/test_structure.py

# Run all tests (if using pytest in future)
# pytest tests/
```

## Test Results

Expected output for successful tests:

```
✅ All tests passed!

Next steps:
1. Set up Supabase credentials in .env
2. Run: python main.py --player-name 'YourName'
```
