import sqlite3
from konfigurasi import DATABASE_NAME

class DatabaseKas:
    def __init__(self):
        self.db_name = DATABASE_NAME

    def connect(self):
        return sqlite3.connect(self.db_name)

    def tambah_kas(self, tanggal, jenis, kategori, keterangan, jumlah):
        with self.connect() as conn:
            conn.execute("""
                INSERT INTO kas (tanggal, jenis, kategori, keterangan, jumlah)
                VALUES (?, ?, ?, ?, ?)
            """, (tanggal, jenis, kategori, keterangan, jumlah))

    def get_semua_kas(self):
        with self.connect() as conn:
            cursor = conn.execute("SELECT * FROM kas ORDER BY tanggal DESC")
            return cursor.fetchall()

    def hapus_kas(self, id_kas):
        with self.connect() as conn:
            conn.execute("DELETE FROM kas WHERE id = ?", (id_kas,))

    def total_kas(self, jenis):
        with self.connect() as conn:
            cursor = conn.execute("SELECT SUM(jumlah) FROM kas WHERE jenis = ?", (jenis,))
            hasil = cursor.fetchone()[0]
            return hasil if hasil else 0

    def set_saldo_awal(self, nominal, tanggal):
        with self.connect() as conn:
            conn.execute("DELETE FROM saldo_awal")
            conn.execute("""
                INSERT INTO saldo_awal (nominal, tanggal)
                VALUES (?, ?)
            """, (nominal, tanggal))

    def get_saldo_awal(self):
        with self.connect() as conn:
            cursor = conn.execute("SELECT nominal FROM saldo_awal LIMIT 1")
            hasil = cursor.fetchone()
            return hasil[0] if hasil else 0

    def get_saldo_akhir(self):
        saldo_awal = self.get_saldo_awal()
        total_pemasukan = self.total_kas("pemasukan")
        total_pengeluaran = self.total_kas("pengeluaran")
        return saldo_awal + total_pemasukan - total_pengeluaran

    def update_kas(self, id_transaksi, tanggal, jenis, kategori, keterangan, jumlah):
        with self.connect() as conn:
            conn.execute("""
                UPDATE kas
                SET tanggal=?, jenis=?, kategori=?, keterangan=?, jumlah=?
                WHERE id=?
            """, (tanggal, jenis, kategori, keterangan, jumlah, id_transaksi))
