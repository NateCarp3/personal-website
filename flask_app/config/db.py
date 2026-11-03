"""Postgres connection helper.

Reads the connection string from the DATABASE_URL environment variable,
which Render sets for you. Locally, set DATABASE_URL to try the comment
form; without it the site still runs and the form shows a friendly note.
"""
import os

import psycopg
from psycopg.rows import dict_row

DATABASE_URL = os.environ.get("DATABASE_URL")


def db_enabled():
    return bool(DATABASE_URL)


def query_db(query, data=None, fetch="all"):
    """Run a query. fetch: "all" (list of dicts), "one" (dict or None) or None."""
    with psycopg.connect(DATABASE_URL, row_factory=dict_row) as conn:
        with conn.cursor() as cur:
            cur.execute(query, data)
            if fetch == "all":
                return cur.fetchall()
            if fetch == "one":
                return cur.fetchone()
            return None


def init_db():
    """Create the comments table if it doesn't exist yet."""
    if not db_enabled():
        return
    query_db(
        """
        CREATE TABLE IF NOT EXISTS comments (
            id SERIAL PRIMARY KEY,
            first_name VARCHAR(100) NOT NULL,
            last_name VARCHAR(100) NOT NULL,
            email VARCHAR(255) NOT NULL,
            comment TEXT NOT NULL,
            created_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
            updated_at TIMESTAMPTZ NOT NULL DEFAULT NOW()
        );
        """,
        fetch=None,
    )
