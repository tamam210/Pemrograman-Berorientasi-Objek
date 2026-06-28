"""
TUGAS 7 - Polymorphism (Method Overriding & Duck Typing)
Pemrograman Berorientasi Objek
"""

# =============================================================
# 1. METHOD OVERRIDING
#    Subclass memberikan implementasi unik pada method warisan
# =============================================================

class Karyawan:
    def __init__(self, nama, gaji):
        self.nama = nama
        self.gaji = gaji

    def kerja(self):
        return f"{self.nama} melakukan pekerjaan umum."

    def info(self):
        return f"[Karyawan] {self.nama} | Gaji: Rp{self.gaji:,}"


class Manager(Karyawan):
    def __init__(self, nama, gaji, divisi):
        super().__init__(nama, gaji)
        self.divisi = divisi

    def kerja(self):
        return f"{self.nama} memimpin divisi {self.divisi}."

    def info(self):
        return f"[Manager] {self.nama} | Divisi: {self.divisi} | Gaji: Rp{self.gaji:,}"


class Engineer(Karyawan):
    def __init__(self, nama, gaji, bahasa):
        super().__init__(nama, gaji)
        self.bahasa = bahasa

    def kerja(self):
        return f"{self.nama} menulis kode dalam {self.bahasa}."

    def info(self):
        return f"[Engineer] {self.nama} | Bahasa: {self.bahasa} | Gaji: Rp{self.gaji:,}"


class Intern(Karyawan):
    def __init__(self, nama, gaji, durasi):
        super().__init__(nama, gaji)
        self.durasi = durasi

    def kerja(self):
        return f"{self.nama} belajar sambil bekerja ({self.durasi} bulan)."

    def info(self):
        return f"[Intern] {self.nama} | Durasi: {self.durasi} bln | Gaji: Rp{self.gaji:,}"


# =============================================================
# 2. DUCK TYPING
#    "Jika ia berjalan seperti bebek dan berbunyi seperti
#     bebek, maka ia adalah bebek."
#    Tipe objek tidak penting; yang penting adalah metode-nya.
# =============================================================

class Bebek:
    def suara(self):
        return "Kwek kwek!"

    def gerak(self):
        return "Bebek berjalan dengan dua kaki."


class Ayam:
    def suara(self):
        return "Petok petok!"

    def gerak(self):
        return "Ayam berjalan dengan dua kaki."


class Kambing:
    def suara(self):
        return "Mbek mbek!"

    def gerak(self):
        return "Kambing berjalan dengan empat kaki."


class Mobil:
    def suara(self):
        return "Vroom vroom!"

    def gerak(self):
        return "Mobil berjalan di atas roda."


# Fungsi yang menerima objek APAPUN selama punya method suara() & gerak()
def tampilkan_hewan(hewan):
    print(f"  Suara: {hewan.suara()}")
    print(f"  Gerak: {hewan.gerak()}")


# =============================================================
# 3. DUCK TYPING EKSTRA — Tipe berbeda, antarmuka sama
#    Contoh lain dengan class yang tidak memiliki hubungan
#    pewarisan sama sekali.
# =============================================================

class Pesawat:
    def terbang(self):
        return "Pesawat terbang di udara."

    def muatan(self):
        return "Membawa penumpang."


class Burung:
    def terbang(self):
        return "Burung terbang dengan sayap."

    def muatan(self):
        return "Tidak membawa muatan."


class PesawatTempel(Pesawat, Burung):
    pass


# Fungsi duck typing — terima apa saja yang punya method terbang()
def terbangkan(objek):
    print(f"  {objek.terbang()}")
    print(f"  {objek.muatan()}")


# =============================================================
# DEMONSTRASI
# =============================================================

print("=" * 65)
print("1. METHOD OVERRIDING")
print("   - Subclass menimpa method kerja() dan info()")
print("     milik class Karyawan dengan implementasi sendiri")
print("=" * 65)

karyawan_list = [
    Manager("Andi", 15_000_000, "Teknologi"),
    Engineer("Budi", 12_000_000, "Python"),
    Intern("Citra", 3_000_000, 6),
]

for k in karyawan_list:
    print(f"\n{k.info()}")
    print(f"  -> {k.kerja()}")

print()

print("=" * 65)
print("2. DUCK TYPING — Bebek, Ayam, Kambing, Mobil")
print('   Selama punya method suara() & gerak(), fungsi')
print("   tampilkan_hewan() bisa menerimanya.")
print("=" * 65)

hewan_list = [Bebek(), Ayam(), Kambing(), Mobil()]
for h in hewan_list:
    print(f"\n  {type(h).__name__}:")
    tampilkan_hewan(h)

print()

print("=" * 65)
print("3. DUCK TYPING — Burung & Pesawat")
print("   Terbang() dan muatan() pada class berbeda.")
print("=" * 65)

for obj in [Burung(), Pesawat(), PesawatTempel()]:
    print(f"\n  {type(obj).__name__}:")
    terbangkan(obj)

print()

print("=" * 65)
print("4. POLYMORPHISM DENGAN len(), iter(), dll.")
print("   Fungsi bawaan Python juga menerapkan polymorphism.")
print("=" * 65)

print(f"\n  len(\"Python\")         => {len('Python')}")
print(f"  len([1, 2, 3, 4])     => {len([1, 2, 3, 4])}")
print(f"  len((1, 2))           => {len((1, 2))}")
print()
print("  Semua punya method __len__() — itulah duck typing!")
