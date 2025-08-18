
from __future__ import annotations
import sqlite3, os
from typing import Iterable
from .models import MaterialMetric
SCHEMA_SQL = """
CREATE TABLE IF NOT EXISTS snapshots(
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  root_dir TEXT NOT NULL,
  created_at TEXT NOT NULL
);
CREATE TABLE IF NOT EXISTS metrics(
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  snapshot_id INTEGER NOT NULL,
  material TEXT NOT NULL,
  source TEXT NOT NULL,
  file_path TEXT NOT NULL,
  weight REAL,
  chance REAL,
  amount_min REAL,
  amount_max REAL,
  stack_min REAL,
  stack_max REAL,
  score REAL,
  FOREIGN KEY(snapshot_id) REFERENCES snapshots(id)
);
"""
class DB:
    def __init__(self, path: str):
        self.path = path
        os.makedirs(os.path.dirname(path), exist_ok=True)
        self.conn = sqlite3.connect(path)
        self.conn.execute("PRAGMA journal_mode=WAL;")
        self.conn.executescript(SCHEMA_SQL)
    def insert_snapshot(self, root_dir: str, created_at: str) -> int:
        cur = self.conn.cursor()
        cur.execute("INSERT INTO snapshots(root_dir, created_at) VALUES(?,?)", (root_dir, created_at))
        self.conn.commit()
        return cur.lastrowid
    def insert_metrics(self, snapshot_id: int, metrics: Iterable[MaterialMetric]):
        rows = []
        for m in metrics:
            rows.append((snapshot_id, m.material, m.source, m.file_path, m.weight, m.chance, m.amount_min, m.amount_max, m.stack_min, m.stack_max, m.availability_score()))
        if rows:  # Only execute if there are rows to insert
            self.conn.executemany("""
                INSERT INTO metrics(snapshot_id, material, source, file_path, weight, chance, amount_min, amount_max, stack_min, stack_max, score)
                VALUES(?,?,?,?,?,?,?,?,?,?,?)
            """, rows)
            self.conn.commit()
    def fetch_snapshot_metrics(self, snapshot_id: int):
        cur = self.conn.cursor()
        cur.execute("SELECT material, source, SUM(score) FROM metrics WHERE snapshot_id=? GROUP BY material, source", (snapshot_id,))
        return cur.fetchall()
    def latest_snapshot_id_for_root(self, root_dir: str):
        cur = self.conn.cursor()
        cur.execute("SELECT id FROM snapshots WHERE root_dir=? ORDER BY id DESC LIMIT 1", (root_dir,))
        row = cur.fetchone()
        return row[0] if row else None
    def close(self):
        self.conn.close()
