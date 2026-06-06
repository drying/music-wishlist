from fastapi import FastAPI, HTTPException
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from pydantic import BaseModel
from typing import Optional
from contextlib import contextmanager
import sqlite3
import os

app = FastAPI()

DB_PATH = "wishlist.db"


@contextmanager
def get_db():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    try:
        yield conn
    finally:
        conn.close()


def init_db():
    with get_db() as conn:
        conn.execute("""
            CREATE TABLE IF NOT EXISTS wishlist (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                title TEXT NOT NULL,
                artist TEXT NOT NULL,
                album TEXT,
                format TEXT DEFAULT 'CD',
                status TEXT DEFAULT 'want',
                memo TEXT,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        """)
        conn.commit()


init_db()


class WishlistItem(BaseModel):
    title: str
    artist: str
    album: Optional[str] = None
    format: str = "CD"
    status: str = "want"
    memo: Optional[str] = None


class WishlistItemUpdate(BaseModel):
    title: Optional[str] = None
    artist: Optional[str] = None
    album: Optional[str] = None
    format: Optional[str] = None
    status: Optional[str] = None
    memo: Optional[str] = None


@app.get("/api/items")
def get_items(status: Optional[str] = None, q: Optional[str] = None):
    query = "SELECT * FROM wishlist WHERE 1=1"
    params = []
    if status:
        query += " AND status = ?"
        params.append(status)
    if q:
        query += " AND (title LIKE ? OR artist LIKE ? OR album LIKE ?)"
        params.extend([f"%{q}%", f"%{q}%", f"%{q}%"])
    query += " ORDER BY created_at DESC"
    with get_db() as conn:
        rows = conn.execute(query, params).fetchall()
    return [dict(r) for r in rows]


@app.post("/api/items", status_code=201)
def create_item(item: WishlistItem):
    with get_db() as conn:
        cur = conn.execute(
            "INSERT INTO wishlist (title, artist, album, format, status, memo) VALUES (?,?,?,?,?,?)",
            (item.title, item.artist, item.album, item.format, item.status, item.memo)
        )
        conn.commit()
        row = conn.execute("SELECT * FROM wishlist WHERE id = ?", (cur.lastrowid,)).fetchone()
    return dict(row)


@app.patch("/api/items/{item_id}")
def update_item(item_id: int, item: WishlistItemUpdate):
    allowed_columns = {"title", "artist", "album", "format", "status", "memo"}
    fields = {k: v for k, v in item.model_dump(exclude_unset=True).items() if k in allowed_columns}
    with get_db() as conn:
        row = conn.execute("SELECT * FROM wishlist WHERE id = ?", (item_id,)).fetchone()
        if not row:
            raise HTTPException(status_code=404, detail="Not found")
        if fields:
            set_clause = ", ".join(f"{k} = ?" for k in fields)
            conn.execute(f"UPDATE wishlist SET {set_clause} WHERE id = ?", [*fields.values(), item_id])
            conn.commit()
        row = conn.execute("SELECT * FROM wishlist WHERE id = ?", (item_id,)).fetchone()
    return dict(row)


@app.delete("/api/items/{item_id}")
def delete_item(item_id: int):
    with get_db() as conn:
        row = conn.execute("SELECT * FROM wishlist WHERE id = ?", (item_id,)).fetchone()
        if not row:
            raise HTTPException(status_code=404, detail="Not found")
        conn.execute("DELETE FROM wishlist WHERE id = ?", (item_id,))
        conn.commit()
    return {"ok": True}


app.mount("/", StaticFiles(directory="static", html=True), name="static")
