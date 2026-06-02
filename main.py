from fastapi import FastAPI, HTTPException
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from pydantic import BaseModel
from typing import Optional
import sqlite3
import os

app = FastAPI()

DB_PATH = "wishlist.db"


def get_db():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn


def init_db():
    conn = get_db()
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
    conn.close()


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
    conn = get_db()
    query = "SELECT * FROM wishlist WHERE 1=1"
    params = []
    if status:
        query += " AND status = ?"
        params.append(status)
    if q:
        query += " AND (title LIKE ? OR artist LIKE ? OR album LIKE ?)"
        params.extend([f"%{q}%", f"%{q}%", f"%{q}%"])
    query += " ORDER BY created_at DESC"
    rows = conn.execute(query, params).fetchall()
    conn.close()
    return [dict(r) for r in rows]


@app.post("/api/items", status_code=201)
def create_item(item: WishlistItem):
    conn = get_db()
    cur = conn.execute(
        "INSERT INTO wishlist (title, artist, album, format, status, memo) VALUES (?,?,?,?,?,?)",
        (item.title, item.artist, item.album, item.format, item.status, item.memo)
    )
    conn.commit()
    row = conn.execute("SELECT * FROM wishlist WHERE id = ?", (cur.lastrowid,)).fetchone()
    conn.close()
    return dict(row)


@app.patch("/api/items/{item_id}")
def update_item(item_id: int, item: WishlistItemUpdate):
    conn = get_db()
    row = conn.execute("SELECT * FROM wishlist WHERE id = ?", (item_id,)).fetchone()
    if not row:
        conn.close()
        raise HTTPException(status_code=404, detail="Not found")
    fields = {k: v for k, v in item.model_dump().items() if v is not None}
    if fields:
        set_clause = ", ".join(f"{k} = ?" for k in fields)
        conn.execute(f"UPDATE wishlist SET {set_clause} WHERE id = ?", [*fields.values(), item_id])
        conn.commit()
    row = conn.execute("SELECT * FROM wishlist WHERE id = ?", (item_id,)).fetchone()
    conn.close()
    return dict(row)


@app.delete("/api/items/{item_id}")
def delete_item(item_id: int):
    conn = get_db()
    row = conn.execute("SELECT * FROM wishlist WHERE id = ?", (item_id,)).fetchone()
    if not row:
        conn.close()
        raise HTTPException(status_code=404, detail="Not found")
    conn.execute("DELETE FROM wishlist WHERE id = ?", (item_id,))
    conn.commit()
    conn.close()
    return {"ok": True}


app.mount("/", StaticFiles(directory="static", html=True), name="static")
