"""
TUGAS 6 - Inheritance, Multiple Inheritance & Diamond Problem
Pemrograman Berorientasi Objek
"""

# =============================================================
# 1. SINGLE INHERITANCE (Pewarisan Tunggal)
# =============================================================

class Hewan:
    def __init__(self, nama, umur):
        self.nama = nama
        self.umur = umur

    def bersuara(self):
        return f"{self.nama} bersuara."

    def info(self):
        return f"[Hewan] {self.nama}, {self.umur} tahun"


class Kucing(Hewan):
    def __init__(self, nama, umur, ras):
        super().__init__(nama, umur)
        self.ras = ras

    def bersuara(self):
        return f"{self.nama}: Meowww!"

    def info(self):
        return f"[Kucing] {self.nama} | Ras: {self.ras} | {self.umur} tahun"


class Anjing(Hewan):
    def __init__(self, nama, umur, jenis):
        super().__init__(nama, umur)
        self.jenis = jenis

    def bersuara(self):
        return f"{self.nama}: Guk guk!"

    def info(self):
        return f"[Anjing] {self.nama} | Jenis: {self.jenis} | {self.umur} tahun"


# =============================================================
# 2. MULTIPLE INHERITANCE & DIAMOND PROBLEM
#    Struktur diamond:
#          Kendaraan
#          /       \
#        Mobil     Kapal
#          \       /
#          Amfibi
#
#    Python menggunakan MRO (Method Resolution Order) & cooperative
#    inheritance (**kwargs) untuk memastikan setiap __init__()
#    dipanggil tepat satu kali.
# =============================================================

class Kendaraan:
    def __init__(self, nama, tahun, **kwargs):
        self.nama = nama
        self.tahun = tahun
        print(f"  [DIAMOND] Kendaraan.__init__({nama})")


class Mobil(Kendaraan):
    def __init__(self, pintu, **kwargs):
        super().__init__(**kwargs)
        self.pintu = pintu
        print(f"  [DIAMOND] Mobil.__init__()")


class Kapal(Kendaraan):
    def __init__(self, berat, **kwargs):
        super().__init__(**kwargs)
        self.berat = berat
        print(f"  [DIAMOND] Kapal.__init__()")


class Amfibi(Mobil, Kapal):
    def __init__(self, nama, tahun, pintu, berat):
        # MRO: Amfibi -> Mobil -> Kapal -> Kendaraan -> object
        # Setiap kelas mengambil parameternya sendiri, sisanya
        # dilewatkan via **kwargs ke super().__init__()
        super().__init__(nama=nama, tahun=tahun, pintu=pintu, berat=berat)
        print(f"  [DIAMOND] Amfibi.__init__({nama})")

    def info(self):
        return (f"[Amfibi] {self.nama} ({self.tahun})\n"
                f"  Pintu: {self.pintu} | Berat: {self.berat} ton")


# =============================================================
# DEMONSTRASI
# =============================================================

print("=" * 65)
print("1. SINGLE INHERITANCE")
print("   - Kucing dan Anjing mewarisi dari Hewan")
print("   - Method overriding: info() dan bersuara()")
print("=" * 65)

kucing1 = Kucing("Mimi", 2, "Persia")
anjing1 = Anjing("Doggy", 3, "Golden Retriever")

print(f"\n{kucing1.info()}")
print(kucing1.bersuara())

print(f"\n{anjing1.info()}")
print(anjing1.bersuara())

print()

print("=" * 65)
print("2. MULTIPLE INHERITANCE & DIAMOND PROBLEM")
print("=" * 65)

print("\nMembuat objek Amfibi (perhatikan urutan __init__):\n")
amfibi1 = Amfibi("Amphicruiser", 2024, 4, 2.5)

print(f"\n{amfibi1.info()}")

print()

print("=" * 65)
print("3. METHOD RESOLUTION ORDER (MRO)")
print("   Urutan pencarian method pada class Amfibi:")
print("=" * 65)
for i, cls in enumerate(Amfibi.__mro__):
    print(f"  {i}. {cls.__name__}")
