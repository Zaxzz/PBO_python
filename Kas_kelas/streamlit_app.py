import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import sqlite3
from datetime import datetime
from konfigurasi import DATE_FORMAT, KATEGORI_PEMASUKAN, KATEGORI_PENGELUARAN, NAMA_KELAS, TAHUN_AJAR
from manajer_kas import ManajerKas

class KasApp:
    def __init__(self):
        self.kas = ManajerKas()
        st.set_page_config(page_title="Aplikasi Kas Kelas", layout="wide")
        self.render_header()
        self.render_sidebar()
        self.render_tabs()

    def render_header(self):
        st.title(f"\U0001F4D8 Kas Kelas {NAMA_KELAS} - {TAHUN_AJAR}")

    def render_sidebar(self):
        with st.sidebar:
            st.header("\U0001F4B0 Saldo")
            saldo_awal = self.kas.ambil_saldo_awal()
            total_pemasukan = self.kas.hitung_total_pemasukan()
            total_pengeluaran = self.kas.hitung_total_pengeluaran()
            saldo_akhir = self.kas.ambil_saldo_akhir()

            st.metric("Saldo Awal", f"Rp {saldo_awal:,.0f}")
            st.metric("Total Pemasukan", f"Rp {total_pemasukan:,.0f}")
            st.metric("Total Pengeluaran", f"Rp {total_pengeluaran:,.0f}")
            st.metric("Saldo Akhir", f"Rp {saldo_akhir:,.0f}")

            with st.expander("\U0001F6E0️ Atur Saldo Awal"):
                nominal = st.number_input("Masukkan Saldo Awal", min_value=0, step=1000, key="input_saldo")
                tanggal = st.date_input("Tanggal Saldo Awal", value=datetime.today(), key="tanggal_saldo")
                if st.button("Simpan Saldo Awal", key="btn_saldo"):
                    self.kas.atur_saldo_awal(nominal, tanggal.strftime(DATE_FORMAT))
                    st.success("Saldo awal berhasil disimpan!")
                    st.experimental_rerun()

    def render_tabs(self):
        tab1, tab2, tab3 = st.tabs(["➕ Tambah Transaksi", "📋 Riwayat Transaksi", "📊 Grafik Kas"])
        with tab1:
            self.render_tambah_transaksi()
        with tab2:
            self.render_riwayat_transaksi()
        with tab3:
            self.render_grafik_kas()

    def render_tambah_transaksi(self):
        st.subheader("Tambah Transaksi Kas")
        col1, col2 = st.columns(2)
        with col1:
            tanggal = st.date_input("Tanggal", value=datetime.today(), key="tanggal_input")
            jenis = st.selectbox("Jenis", ["pemasukan", "pengeluaran"], key="jenis_input")
        with col2:
            kategori = st.selectbox("Kategori", KATEGORI_PEMASUKAN if jenis == "pemasukan" else KATEGORI_PENGELUARAN, key="kategori_input")
            jumlah = st.number_input("Jumlah (Rp)", min_value=0, step=1000, key="jumlah_input")
        keterangan = st.text_input("Keterangan (opsional)", key="ket_input")

        if st.button("Simpan Transaksi", key="btn_simpan"):
            try:
                self.kas.tambah_transaksi(tanggal.strftime(DATE_FORMAT), jenis, kategori, keterangan, jumlah)
                st.success("Transaksi berhasil ditambahkan!")
                st.experimental_rerun()
            except Exception as e:
                st.error(f"Gagal menambahkan transaksi: {e}")

    def render_riwayat_transaksi(self):
        st.subheader("Riwayat Transaksi Kas")
        data = self.kas.tampilkan_semua_transaksi()

        if data:
            for transaksi in data:
                id_, tgl, jenis, kategori, ket, jumlah = transaksi
                with st.container():
                    col1, col2, col3, col4, col5 = st.columns([2, 2, 3, 1, 1])
                    col1.markdown(f"📅 **{tgl}**")
                    col2.markdown(f"**{jenis.title()}** - {kategori}")
                    col3.markdown(f"📝 _{ket or '-'}_")
                    col4.markdown(f"**Rp {jumlah:,.0f}**")

                    if col5.button("🗑️", key=f"hapus_{id_}"):
                        self.kas.hapus_transaksi(id_)
                        st.experimental_rerun()

                    if col5.button("✏️", key=f"edit_{id_}"):
                        st.session_state.editing = id_

                if "editing" in st.session_state and st.session_state.editing == id_:
                    self.render_form_edit(id_, tgl, jenis, kategori, ket, jumlah)
                    st.markdown("<hr style='border: 1px solid white;'>", unsafe_allow_html=True)
        else:
            st.info("Belum ada transaksi kas yang tercatat.")

    def render_form_edit(self, id_, tgl, jenis, kategori, ket, jumlah):
        st.markdown("### ✏️ Edit Transaksi")
        with st.form(f"form_edit_{id_}"):
            tanggal_edit = st.date_input("Tanggal", value=datetime.strptime(tgl, DATE_FORMAT))
            jenis_edit = st.selectbox("Jenis", ["pemasukan", "pengeluaran"], index=0 if jenis == "pemasukan" else 1)
            kategori_list = KATEGORI_PEMASUKAN if jenis_edit == "pemasukan" else KATEGORI_PENGELUARAN
            kategori_edit = st.selectbox("Kategori", kategori_list, index=kategori_list.index(kategori) if kategori in kategori_list else 0)
            jumlah_edit = st.number_input("Jumlah (Rp)", value=jumlah, min_value=0, step=1000)
            ket_edit = st.text_input("Keterangan (opsional)", value=ket or "")
            simpan_edit = st.form_submit_button("Simpan Perubahan")
            batal_edit = st.form_submit_button("Batal")

            if simpan_edit:
                try:
                    self.kas.update_transaksi(id_, tanggal_edit.strftime(DATE_FORMAT), jenis_edit, kategori_edit, ket_edit, jumlah_edit)
                    st.success("✅ Transaksi berhasil diperbarui!")
                    del st.session_state.editing
                    st.experimental_rerun()
                except Exception as e:
                    st.error(f"Gagal mengedit transaksi: {e}")
            elif batal_edit:
                del st.session_state.editing
                st.experimental_rerun()

    def render_grafik_kas(self):
        st.subheader("📊 Grafik Kas Masuk dan Keluar")

        # Koneksi dan ambil data
        conn = sqlite3.connect("kas_kelas.db")
        query = "SELECT tanggal, jenis, jumlah FROM kas"
        df = pd.read_sql_query(query, conn)
        conn.close()

        if df.empty:
            st.info("Belum ada data transaksi untuk ditampilkan.")
            return

        # Proses data
        df['tanggal'] = pd.to_datetime(df['tanggal'])
        df['bulan'] = df['tanggal'].dt.to_period('M').astype(str)
        df_grouped = df.groupby(['bulan', 'jenis'])['jumlah'].sum().unstack().fillna(0)

        # Tabel data agregasi
        st.dataframe(df_grouped, use_container_width=True)

        # Grafik
        fig, ax = plt.subplots()
        df_grouped.plot(kind='bar', ax=ax)
        ax.set_title("Kas Masuk dan Keluar per Bulan")
        ax.set_xlabel("Bulan")
        ax.set_ylabel("Jumlah (Rp)")
        ax.legend(["Pemasukan", "Pengeluaran"])
        st.pyplot(fig)

if __name__ == "__main__":
    KasApp()
