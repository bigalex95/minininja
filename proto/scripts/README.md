# Setup Scripts

Automated setup scripts for easy project configuration.

## Available Scripts

### `setup.sh`

Main setup script that installs dependencies and creates .env file.

**Usage:**

```bash
./scripts/setup.sh
# or:
bash scripts/setup.sh
```

**What it does:**

- Creates `.env` file from `.env.example` (if not exists)
- Installs Python dependencies using `uv` or `pip`
- Displays next steps for Supabase setup

### `setup_supabase.py`

Interactive Supabase configuration helper.

**Usage:**

```bash
python scripts/setup_supabase.py
```

**What it does:**

- Guides you through Supabase account creation
- Helps create the leaderboard table
- Collects your API credentials
- Creates/updates `.env` file
- Tests the connection

### `setup_database.py` ⭐ **Important!**

Verifies database table setup and provides SQL to create it.

**Usage:**

```bash
python scripts/setup_database.py
```

**What it does:**

- Checks if `.env` credentials are configured
- Tests connection to Supabase
- Verifies if `leaderboard` table exists
- Shows SQL to create the table if missing
- Displays current leaderboard stats

**Run this after setting up Supabase credentials!**

## Quick Setup

For first-time setup:

```bash
# 1. Run main setup
./scripts/setup.sh

# 2. Configure Supabase (interactive)
python scripts/setup_supabase.py

# 3. Create database table and verify
python scripts/setup_database.py

# 4. Start playing!
python main.py --player-name "YourName" --show-leaderboard
```

## 🚨 Common Issue: Table Not Found

If you get an error about the table not existing:

```bash
# Run this to see the SQL you need
python scripts/setup_database.py

# Then go to Supabase SQL Editor and run the SQL
# See: QUICK_FIX.md for step-by-step guide
```

## Manual Setup

If you prefer manual setup:

1. Copy `.env.example` to `.env`
2. Follow [docs/SUPABASE_SETUP.md](../docs/SUPABASE_SETUP.md)
3. Edit `.env` with your credentials
4. Run: `uv sync` or `pip install -e .`
