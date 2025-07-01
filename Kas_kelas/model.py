# model.py

from dataclasses import dataclass

@dataclass
class TransaksiKas:
    id: int
    tanggal: str
    jenis: str         
    kategori: str
    keterangan: str
    jumlah: int

@dataclass
class User:
    id: int
    nama: str
    peran: str          

@dataclass
class SaldoAwal:
    id: int
    nominal: int
    tanggal: str
