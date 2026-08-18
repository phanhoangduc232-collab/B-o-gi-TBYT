# -*- coding: utf-8 -*-
import sqlite3
import os

# DATA_DIR: thu muc luu du lieu ben vung (persistent). Khi deploy tren Render/co dia
# persistent disk, dat bien moi truong DATA_DIR tro toi duong dan da mount (vd /var/data).
# Mac dinh khi chay local la thu muc "instance" ngay canh file nay.
DATA_DIR = os.environ.get(
    "DATA_DIR", os.path.join(os.path.dirname(os.path.abspath(__file__)), "instance")
)
os.makedirs(DATA_DIR, exist_ok=True)
DB_PATH = os.path.join(DATA_DIR, "data.sqlite3")


def get_db():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    conn.execute("PRAGMA foreign_keys = ON")
    return conn


SCHEMA = """
CREATE TABLE IF NOT EXISTS vendors (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    ten_ncc TEXT NOT NULL,
    mst TEXT NOT NULL UNIQUE,
    dia_chi TEXT,
    nguoi_lien_he TEXT,
    sdt TEXT,
    email TEXT,
    password_hash TEXT NOT NULL,
    created_at TEXT NOT NULL,
    submitted_at TEXT
);

CREATE TABLE IF NOT EXISTS quote_items (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    vendor_id INTEGER NOT NULL REFERENCES vendors(id) ON DELETE CASCADE,
    ma_danh_muc TEXT NOT NULL,
    ten_thuong_mai TEXT,
    model TEXT,
    hang_sx TEXT,
    xuat_xu TEXT,
    don_gia INTEGER,
    ngay_bao_gia TEXT,
    created_at TEXT NOT NULL
);

CREATE TABLE IF NOT EXISTS maintenance_items (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    vendor_id INTEGER NOT NULL REFERENCES vendors(id) ON DELETE CASCADE,
    ma_danh_muc TEXT NOT NULL,
    don_gia_baotri INTEGER,
    ghi_chu TEXT,
    created_at TEXT NOT NULL
);

CREATE TABLE IF NOT EXISTS files (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    vendor_id INTEGER NOT NULL REFERENCES vendors(id) ON DELETE CASCADE,
    tag TEXT,
    original_filename TEXT NOT NULL,
    stored_filename TEXT NOT NULL,
    uploaded_at TEXT NOT NULL
);
"""


def init_db():
    conn = get_db()
    conn.executescript(SCHEMA)
    conn.commit()
    conn.close()


if __name__ == "__main__":
    init_db()
    print("Database initialized at", DB_PATH)
