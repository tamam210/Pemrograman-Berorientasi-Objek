class Produk:
    def __init__(self, nama, harga, stok):
        self.nama = nama
        self.harga = harga
        self.stok = stok

    def __str__(self):
        return f"[Produk] {self.nama} | Harga: Rp{self.harga:,} | Stok: {self.stok}"

    def __eq__(self, other):
        if not isinstance(other, Produk):
            return NotImplemented
        return self.harga == other.harga

    def __lt__(self, other):
        if not isinstance(other, Produk):
            return NotImplemented
        return self.harga < other.harga

    def __gt__(self, other):
        if not isinstance(other, Produk):
            return NotImplemented
        return self.harga > other.harga


# Instansiasi 3 object berbeda
produk1 = Produk("Laptop Gaming", 15000000, 10)
produk2 = Produk("Mouse Wireless", 350000, 50)
produk3 = Produk("Keyboard Mechanical", 1200000, 25)

# Tampilkan representasi teks (__str__)
print(produk1)
print(produk2)
print(produk3)
print()

# Pengujian perbandingan antar objek
print(f"Apakah {produk1.nama} == {produk2.nama}? {produk1 == produk2}")
print(f"Apakah {produk2.nama} < {produk3.nama}? {produk2 < produk3}")
print(f"Apakah {produk3.nama} > {produk1.nama}? {produk3 > produk1}")