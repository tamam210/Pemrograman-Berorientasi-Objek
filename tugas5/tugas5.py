"""
TUGAS 5 - Encapsulation (Getter, Setter & Validasi)
Pemrograman Berorientasi Objek
"""

class RekeningBank:
    """
    Encapsulation: atribut __saldo dan __pin bersifat private (__)
    sehingga tidak bisa diakses langsung dari luar kelas.
    Akses hanya melalui metode getter/setter yang terkontrol.
    """

    def __init__(self, pemilik, no_rekening, saldo_awal, pin):
        self.pemilik = pemilik
        self.no_rekening = no_rekening
        self.__saldo = saldo_awal       # Private attribute
        self.__pin = pin                 # Private attribute
        self.__log_transaksi = []        # Private attribute

    # --- Getter ---
    def get_saldo(self, pin):
        if pin == self.__pin:
            return f"Saldo {self.pemilik}: Rp{self.__saldo:,}"
        return "[AKSES DITOLAK] PIN salah!"

    def get_info_rekening(self):
        return f"[REKENING] {self.pemilik} | No: {self.no_rekening}"

    # --- Setter dengan validasi ---
    def setor(self, jumlah):
        if jumlah <= 0:
            return "[ERROR] Jumlah setor harus positif!"
        self.__saldo += jumlah
        self.__log_transaksi.append(f"Setor Rp{jumlah:,}")
        return f"[OK] Setor Rp{jumlah:,} berhasil. Saldo: Rp{self.__saldo:,}"

    def tarik(self, jumlah, pin):
        if pin != self.__pin:
            return "[AKSES DITOLAK] PIN salah!"
        if jumlah <= 0:
            return "[ERROR] Jumlah tarik harus positif!"
        if jumlah > self.__saldo:
            return f"[ERROR] Saldo tidak cukup! Saldo: Rp{self.__saldo:,}"
        self.__saldo -= jumlah
        self.__log_transaksi.append(f"Tarik Rp{jumlah:,}")
        return f"[OK] Tarik Rp{jumlah:,} berhasil. Saldo: Rp{self.__saldo:,}"

    def ganti_pin(self, pin_lama, pin_baru):
        if pin_lama != self.__pin:
            return "[AKSES DITOLAK] PIN lama salah!"
        if len(str(pin_baru)) < 4:
            return "[ERROR] PIN baru minimal 4 digit!"
        self.__pin = pin_baru
        return "[OK] PIN berhasil diganti."

    def tampilkan_log(self, pin):
        if pin != self.__pin:
            return "[AKSES DITOLAK] PIN salah!"
        if not self.__log_transaksi:
            return "[INFO] Belum ada transaksi."
        return "\n".join([f"  {i+1}. {log}" for i, log in enumerate(self.__log_transaksi)])


# --- Demonstrasi ---
print("=" * 55)
print("ENCAPSULATION — Rekening Bank")
print("Atribut __saldo, __pin, __log_transaksi bersifat private")
print("=" * 55)

rek = RekeningBank("Andi Pratama", "123-456-789", 1_000_000, 1234)

# Akses via getter (dengan PIN)
print(f"\n{rek.get_info_rekening()}")
print(rek.get_saldo(1234))

# Setter (setor & tarik dengan validasi)
print(f"\n{rek.setor(500_000)}")
print(rek.tarik(200_000, 1234))
print(rek.tarik(2_000_000, 1234))   # Gagal: saldo tidak cukup
print(rek.tarik(-5000, 1234))       # Gagal: jumlah negatif

# Akses langsung ke atribut private (akan error)
print("\n" + "=" * 55)
print("DEMO: Akses langsung ke atribut private")
print("=" * 55)
try:
    print(rek.__saldo)
except AttributeError as e:
    print(f"  [ERROR] {e}")

# Tapi masih bisa diakses via name mangling (tidak disarankan)
print("\n  (Name mangling) __saldo via _RekeningBank__saldo:")
print(f"  {rek._RekeningBank__saldo}")

# Ganti PIN
print("\n" + "=" * 55)
print("GANTI PIN & LOG TRANSAKSI")
print("=" * 55)
print(rek.ganti_pin(1234, 5678))
print(rek.tarik(100_000, 5678))       # PIN baru berfungsi
print(rek.tarik(50_000, 1234))        # PIN lama ditolak

# Log transaksi
print(f"\nLog Transaksi:")
print(rek.tampilkan_log(5678))
