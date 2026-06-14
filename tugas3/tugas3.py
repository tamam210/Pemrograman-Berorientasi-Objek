class Karyawan:
    """
    Class untuk manajemen data karyawan.
    Demonstrasi perbedaan Instance Method vs Static Method.
    """
    
    def __init__(self, nama, jabatan, gaji_pokok):
        self.nama = nama
        self.jabatan = jabatan
        self.gaji_pokok = gaji_pokok

    def tampilkan_info(self):
        """Instance Method 1: Menampilkan atribut object"""
        return f"[INFO] {self.nama} | Jabatan: {self.jabatan} | Gaji Pokok: Rp{self.gaji_pokok:,}"

    def hitung_bonus(self, persentase):
        """Instance Method 2: Menghitung bonus berdasarkan gaji object"""
        bonus = self.gaji_pokok * (persentase / 100)
        return f"[BONUS] {self.nama} mendapat bonus sebesar: Rp{bonus:,}"

    @staticmethod
    def hitung_pajak(gaji):
        """Static Method: Menghitung pajak secara umum, tidak terikat object"""
        if gaji > 10000000:
            return gaji * 0.10
        return gaji * 0.05


# Instansiasi & Pengujian
karyawan1 = Karyawan("Andi", "Software Engineer", 15000000)
karyawan2 = Karyawan("Budi", "Junior Admin", 6000000)

print(karyawan1.tampilkan_info())
print(karyawan1.hitung_bonus(10))
print("-" * 40)
print(karyawan2.tampilkan_info())
print(karyawan2.hitung_bonus(15))

print(f"\n[PAJAK via Class] Andi: Rp{Karyawan.hitung_pajak(15000000):,}")
print(f"[PAJAK via Object] Budi: Rp{karyawan2.hitung_pajak(6000000):,}")