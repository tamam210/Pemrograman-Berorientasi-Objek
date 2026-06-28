"""
TUGAS 8 - Exception Handling
Pemrograman Berorientasi Objek
"""

# =============================================================
# 1. CUSTOM EXCEPTION
#    Exception khusus untuk logika bisnis
# =============================================================

class SaldoError(Exception):
    """Base exception untuk error saldo."""
    pass

class SaldoTidakCukup(SaldoError):
    def __init__(self, saldo, jumlah):
        self.saldo = saldo
        self.jumlah = jumlah
        super().__init__(f"Saldo tidak cukup! Saldo: Rp{saldo:,}, Tarik: Rp{jumlah:,}")

class JumlahNegatif(SaldoError):
    def __init__(self, jumlah):
        self.jumlah = jumlah
        super().__init__(f"Jumlah tidak valid: Rp{jumlah:,}. Harus positif!")

class BatasTransferError(SaldoError):
    def __init__(self, jumlah, batas):
        self.jumlah = jumlah
        self.batas = batas
        super().__init__(f"Transfer Rp{jumlah:,} melebihi batas Rp{batas:,}!")

class RekeningNotFound(Exception):
    def __init__(self, norek):
        self.norek = norek
        super().__init__(f"Rekening {norek} tidak ditemukan!")

# =============================================================
# 2. CLASS DENGAN EXCEPTION HANDLING
#    Exception menjaga integritas objek
# =============================================================

class Rekening:
    def __init__(self, norek, pemilik, saldo_awal=0):
        if saldo_awal < 0:
            raise JumlahNegatif(saldo_awal)
        self.norek = norek
        self.pemilik = pemilik
        self.saldo = saldo_awal

    def setor(self, jumlah):
        if jumlah <= 0:
            raise JumlahNegatif(jumlah)
        self.saldo += jumlah
        return f"Setor Rp{jumlah:,} berhasil. Saldo: Rp{self.saldo:,}"

    def tarik(self, jumlah):
        if jumlah <= 0:
            raise JumlahNegatif(jumlah)
        if jumlah > self.saldo:
            raise SaldoTidakCukup(self.saldo, jumlah)
        self.saldo -= jumlah
        return f"Tarik Rp{jumlah:,} berhasil. Saldo: Rp{self.saldo:,}"

    def transfer(self, tujuan, jumlah, batas_transfer=10_000_000):
        if jumlah <= 0:
            raise JumlahNegatif(jumlah)
        if jumlah > batas_transfer:
            raise BatasTransferError(jumlah, batas_transfer)
        if jumlah > self.saldo:
            raise SaldoTidakCukup(self.saldo, jumlah)
        self.saldo -= jumlah
        tujuan.saldo += jumlah
        return (f"Transfer Rp{jumlah:,} ke {tujuan.pemilik} "
                f"({tujuan.norek}) berhasil. Saldo: Rp{self.saldo:,}")

    def info(self):
        return f"[{self.norek}] {self.pemilik} — Rp{self.saldo:,}"


class Bank:
    def __init__(self, nama):
        self.nama = nama
        self.rekening_dict = {}

    def tambah_rekening(self, rekening):
        self.rekening_dict[rekening.norek] = rekening

    def cari_rekening(self, norek):
        if norek not in self.rekening_dict:
            raise RekeningNotFound(norek)
        return self.rekening_dict[norek]

    def proses_transfer(self, dari_norek, ke_norek, jumlah):
        pengirim = self.cari_rekening(dari_norek)
        penerima = self.cari_rekening(ke_norek)
        return pengirim.transfer(penerima, jumlah)


# =============================================================
# DEMONSTRASI
# =============================================================

print("=" * 65)
print("1. CUSTOM EXCEPTION")
print("   Exception khusus untuk logika bisnis perbankan:")
print("   - SaldoTidakCukup | JumlahNegatif | BatasTransferError")
print("   - RekeningNotFound")
print("=" * 65)

try:
    raise JumlahNegatif(-50000)
except JumlahNegatif as e:
    print(f"\n  [ERROR] {e}")

try:
    raise SaldoTidakCukup(100_000, 500_000)
except SaldoTidakCukup as e:
    print(f"  [ERROR] {e}")

print()

print("=" * 65)
print("2. TRY-EXCEPT-ELSE-FINALLY")
print("   else => jalan jika tidak ada error")
print("   finally => jalan APAPUN yang terjadi")
print("=" * 65)

for nilai in [50000, -10000, 200000]:
    print(f"\n  >> Mencoba setor Rp{nilai:,}")
    rek = Rekening("111", "Test", 100_000)
    try:
        pesan = rek.setor(nilai)
    except JumlahNegatif as e:
        print(f"     [ERROR] {e}")
    else:
        print(f"     [OK] {pesan}")
    finally:
        print(f"     [FINALLY] Saldo akhir: Rp{rek.saldo:,}")

print()

print("=" * 65)
print("3. RAISE — Menjaga integritas objek")
print("   Constructor Rekening() menolak saldo negatif")
print("=" * 65)

try:
    rek_gagal = Rekening("999", "Gagal", -1_000_000)
except JumlahNegatif as e:
    print(f"\n  [ERROR] Gagal buat rekening: {e}")

rek_berhasil = Rekening("001", "Andi", 500_000)
print(f"  [OK] Rekening berhasil: {rek_berhasil.info()}")

print()

print("=" * 65)
print("4. SKENARIO LENGKAP — Transfer antar rekening")
print("=" * 65)

bank = Bank("Bank OOP")
andi = Rekening("001", "Andi", 20_000_000)
budi = Rekening("002", "Budi", 5_000_000)
citra = Rekening("003", "Citra", 2_000_000)

bank.tambah_rekening(andi)
bank.tambah_rekening(budi)
bank.tambah_rekening(citra)

print(f"\n  Sebelum transfer:")
print(f"    {andi.info()}")
print(f"    {budi.info()}")

skenario = [
    ("Transfer normal",   "transfer", "001", "002", 3_000_000),
    ("Saldo tidak cukup", "transfer", "001", "002", 100_000_000),
    ("Rekening tidak ada","transfer", "001", "999", 1_000_000),
    ("Jumlah negatif",    "transfer", "001", "002", -5000),
    ("Melebihi batas",    "transfer", "001", "002", 15_000_000),
]

for label, aksi, dr, ke, jml in skenario:
    print(f"\n  [{label}]")
    try:
        if aksi == "transfer":
            hasil = bank.proses_transfer(dr, ke, jml)
            print(f"    [OK] {hasil}")
    except SaldoTidakCukup as e:
        print(f"    [ERROR SALDO] {e}")
    except RekeningNotFound as e:
        print(f"    [ERROR REKENING] {e}")
    except JumlahNegatif as e:
        print(f"    [ERROR JUMLAH] {e}")
    except BatasTransferError as e:
        print(f"    [ERROR BATAS] {e}")
    finally:
        print(f"    {andi.info()}")
        print(f"    {budi.info()}")
