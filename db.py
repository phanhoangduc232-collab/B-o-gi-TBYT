# -*- coding: utf-8 -*-
import os
import sqlite3
import psycopg2
from psycopg2.extras import RealDictCursor

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DATA_DIR = os.environ.get("DATA_DIR", os.path.join(BASE_DIR, "instance"))
os.makedirs(DATA_DIR, exist_ok=True)
DB_PATH = os.path.join(DATA_DIR, "data.sqlite3")

DATABASE_URL = os.environ.get("DATABASE_URL")

def get_db():
    if DATABASE_URL:
        # Sử dụng PostgreSQL trên Render
        conn = psycopg2.connect(DATABASE_URL, cursor_factory=RealDictCursor)
        conn.autocommit = True
        return conn
    else:
        # Chạy SQLite khi test trên máy tính cá nhân
        conn = sqlite3.connect(DB_PATH)
        conn.row_factory = sqlite3.Row
        conn.execute("PRAGMA foreign_keys = ON")
        return conn

def init_db():
    conn = get_db()
    cur = conn.cursor()
    if DATABASE_URL:
        # Schema cho PostgreSQL
        cur.execute("""
            CREATE TABLE IF NOT EXISTS vendors (
                id SERIAL PRIMARY KEY,
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
                id SERIAL PRIMARY KEY,
                vendor_id INTEGER NOT NULL REFERENCES vendors(id) ON DELETE CASCADE,
                ma_danh_muc TEXT NOT NULL,
                ten_thuong_mai TEXT,
                model TEXT,
                hang_sx TEXT,
                xuat_xu TEXT,
                don_gia BIGINT,
                ngay_bao_gia TEXT,
                created_at TEXT NOT NULL
            );

            CREATE TABLE IF NOT EXISTS maintenance_items (
                id SERIAL PRIMARY KEY,
                vendor_id INTEGER NOT NULL REFERENCES vendors(id) ON DELETE CASCADE,
                ma_danh_muc TEXT NOT NULL,
                don_gia_baotri BIGINT,
                ghi_chu TEXT,
                created_at TEXT NOT NULL
            );

            CREATE TABLE IF NOT EXISTS files (
                id SERIAL PRIMARY KEY,
                vendor_id INTEGER NOT NULL REFERENCES vendors(id) ON DELETE CASCADE,
                tag TEXT,
                original_filename TEXT NOT NULL,
                stored_filename TEXT NOT NULL,
                uploaded_at TEXT NOT NULL
            );
        """)
    else:
        # Schema cho SQLite
        cur.executescript("""
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
        """)
        conn.commit()
    conn.close()

if __name__ == "__main__":
    init_db()
    print("Database initialized successfully.")
