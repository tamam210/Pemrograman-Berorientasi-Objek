class Kendaraan:
    # Constructor: inisialisasi atribut saat object dibuat
    def __init__(self, merek, tipe, tahun, warna="Hitam"):
        self.merek = merek
        self.tipe = tipe
        self.tahun = tahun
        self.warna = warna
        self.nyala = False  # status mesin

    # Method: perilaku objek
    def nyalakan_mesin(self):
        if not self.nyala:
            self.nyala = True
            print(f"[INFO] Mesin {self.merek} {self.tipe} dinyalakan.")
        else:
            print("[WARNING] Mesin sudah menyala.")

    def matikan_mesin(self):
        if self.nyala:
            self.nyala = False
            print(f"[INFO] Mesin {self.merek} {self.tipe} dimatikan.")
        else:
            print("[WARNING] Mesin sudah mati.")

    def info(self):
        status = "ON" if self.nyala else "OFF"
        print(f"[KENDARAAN] {self.merek} {self.tipe} ({self.tahun}) | Warna: {self.warna} | Mesin: {status}")


# === Membuat Object (Instance) ===
motor1 = Kendaraan("Honda", "Vario 125", 2023, "Merah")
mobil1 = Kendaraan("Toyota", "Avanza", 2021)  # warna default "Hitam"

# === Menggunakan Object ===
motor1.info()
motor1.nyalakan_mesin()
motor1.info()

print("-" * 40)

mobil1.info()
mobil1.nyalakan_mesin()
mobil1.matikan_mesin()