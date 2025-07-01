from database import DatabaseKas

class ManajerKas:
    def __init__(self):
        self.db = DatabaseKas()

    def tambah_transaksi(self, tanggal, jenis, kategori, keterangan, jumlah):
        if not tanggal or not jenis or not jumlah:
            raise ValueError("Tanggal, jenis, dan jumlah tidak boleh kosong.")
        if jenis not in ['pemasukan', 'pengeluaran']:
            raise ValueError("Jenis harus 'pemasukan' atau 'pengeluaran'.")
        self.db.tambah_kas(tanggal, jenis, kategori, keterangan, jumlah)

    def tampilkan_semua_transaksi(self):
        return self.db.get_semua_kas()

    def hapus_transaksi(self, id_transaksi):
        self.db.hapus_kas(id_transaksi)

    def hitung_total_pemasukan(self):
        return self.db.total_kas("pemasukan")

    def hitung_total_pengeluaran(self):
        return self.db.total_kas("pengeluaran")

    def atur_saldo_awal(self, nominal, tanggal):
        self.db.set_saldo_awal(nominal, tanggal)

    def ambil_saldo_awal(self):
        return self.db.get_saldo_awal()

    def ambil_saldo_akhir(self):
        return self.db.get_saldo_akhir()

    def update_transaksi(self, id_transaksi, tanggal, jenis, kategori, keterangan, jumlah):
        self.db.update_kas(id_transaksi, tanggal, jenis, kategori, keterangan, jumlah)
