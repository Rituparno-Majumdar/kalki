"""
Initialise the Kalki PostgreSQL and DuckDB databases.

Usage:
    python scripts/setup_db.py                  # uses DATABASE_URL from .env
    python scripts/setup_db.py --dry-run        # print SQL without executing
    python scripts/setup_db.py --reset          # drop and recreate all tables (dev only)

Author: Rituparno Majumdar
"""

import argparse
import os
import sys
from pathlib import Path

from dotenv import load_dotenv
from rich.console import Console

console = Console()
load_dotenv()

SQL_FILE = Path(__file__).parent / "init_db.sql"


def run_postgres(dry_run: bool = False, reset: bool = False) -> None:
    try:
        import psycopg2
    except ImportError:
        console.print("[red]psycopg2 not installed. Run: pip install psycopg2-binary[/red]")
        sys.exit(1)

    url = os.getenv("DATABASE_URL")
    if not url:
        console.print("[red]DATABASE_URL not set. Copy .env.example to .env and fill it in.[/red]")
        sys.exit(1)

    sql = SQL_FILE.read_text()

    if dry_run:
        console.print("[yellow]--- DRY RUN: SQL that would be executed ---[/yellow]")
        console.print(sql)
        return

    conn = psycopg2.connect(url)
    conn.autocommit = True
    cur = conn.cursor()

    if reset:
        console.print("[bold red]Dropping all Kalki tables...[/bold red]")
        cur.execute("""
            DROP TABLE IF EXISTS kalki_briefings CASCADE;
            DROP TABLE IF EXISTS kalki_signals CASCADE;
            DROP TABLE IF EXISTS kalki_records CASCADE;
        """)
        console.print("[yellow]Tables dropped.[/yellow]")

    console.print("Creating tables...")
    cur.execute(sql)
    console.print("[green]PostgreSQL schema ready.[/green]")

    cur.close()
    conn.close()


def run_duckdb(dry_run: bool = False) -> None:
    try:
        import duckdb
    except ImportError:
        console.print("[red]duckdb not installed. Run: pip install duckdb[/red]")
        sys.exit(1)

    db_path = os.getenv("DUCKDB_PATH", "./data/kalki_analytics.duckdb")
    Path(db_path).parent.mkdir(parents=True, exist_ok=True)

    if dry_run:
        console.print(f"[yellow]DRY RUN: would create DuckDB at {db_path}[/yellow]")
        return

    con = duckdb.connect(db_path)

    # Mirror key tables in DuckDB for analytical queries
    con.execute("""
        CREATE TABLE IF NOT EXISTS kalki_records (
            id                TEXT PRIMARY KEY,
            source_name       TEXT NOT NULL,
            module            TEXT NOT NULL,
            state             TEXT NOT NULL,
            district          TEXT NOT NULL,
            district_lgd_code TEXT,
            record_timestamp  TIMESTAMP NOT NULL,
            data              JSON,
            data_quality_score DOUBLE
        )
    """)

    con.execute("""
        CREATE TABLE IF NOT EXISTS kalki_signals (
            id               TEXT PRIMARY KEY,
            module           TEXT NOT NULL,
            signal_type      TEXT NOT NULL,
            severity         TEXT NOT NULL,
            state            TEXT NOT NULL,
            district         TEXT NOT NULL,
            period_start     TIMESTAMP NOT NULL,
            period_end       TIMESTAMP NOT NULL,
            value            JSON,
            confidence       DOUBLE,
            demographic_flag BOOLEAN DEFAULT FALSE,
            generated_at     TIMESTAMP
        )
    """)

    con.close()
    console.print(f"[green]DuckDB analytics store ready at {db_path}[/green]")


def main() -> None:
    parser = argparse.ArgumentParser(description="Initialise Kalki databases")
    parser.add_argument("--dry-run", action="store_true", help="Print SQL without executing")
    parser.add_argument(
        "--reset",
        action="store_true",
        help="Drop and recreate all tables (dev only, data will be lost)",
    )
    args = parser.parse_args()

    console.print("[bold]Kalki database setup[/bold]")

    run_postgres(dry_run=args.dry_run, reset=args.reset)
    run_duckdb(dry_run=args.dry_run)

    if not args.dry_run:
        console.print("\n[bold green]Setup complete.[/bold green]")
        console.print("Next: [cyan]make dev[/cyan] to start the full stack")


if __name__ == "__main__":
    main()
