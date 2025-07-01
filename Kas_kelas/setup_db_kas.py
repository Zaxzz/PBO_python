# setup_db_kas.py

import sqlite3
from konfigurasi import DATABASE_NAME

def buat_tabel():
    conn = sqlite3.connect(DATABASE_NAME)
    cursor = conn.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nama TEXT NOT NULL,
            peran TEXT CHECK(peran IN ('bendahara', 'ketua', 'anggota')) NOT NULL
        )
    """)

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS kas (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            tanggal TEXT NOT NULL,
            jenis TEXT CHECK(jenis IN ('pemasukan', 'pengeluaran')) NOT NULL,
            kategori TEXT,
            keterangan TEXT,
            jumlah INTEGER NOT NULL
        )
    """)

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS saldo_awal (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nominal INTEGER NOT NULL,
            tanggal TEXT NOT NULL
        )
    """)

    conn.commit()
    conn.close()
    print("Tabel berhasil dibuat atau sudah tersedia.")

if __name__ == "__main__":
    buat_tabel()
