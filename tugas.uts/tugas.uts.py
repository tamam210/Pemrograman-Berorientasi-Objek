"""

Konsep OOP yang Diterapkan:
  1. Encapsulation  → Melindungi data internal (atribut private/protected)
  2. Inheritance    → Pewarisan kelas Pengguna → Admin & Penumpang
  3. Polymorphism   → Metode hitung_harga_akhir() berbeda tiap jenis tiket
"""

import uuid
import datetime
import os


# ============================================================
# SECTION 1: KELAS DASAR - PENGGUNA (BASE CLASS)
# Konsep: ENCAPSULATION + INHERITANCE
# ============================================================

class Pengguna:
    """
    Kelas induk (base class) untuk semua pengguna sistem.
    Konsep OOP: Encapsulation — atribut disimpan sebagai protected (_)
                Inheritance   — diturunkan ke Admin dan Penumpang
    """

    def __init__(self, nama: str, email: str, telepon: str):
        # Protected attributes (konvensi _ = tidak diakses langsung dari luar)
        self._nama = nama
        self._email = email
        self._telepon = telepon
        self._id_pengguna = str(uuid.uuid4())[:8].upper()

    # --- Getter (akses data melalui metode, bukan langsung) ---
    def get_nama(self) -> str:
        return self._nama

    def get_email(self) -> str:
        return self._email

    def get_id(self) -> str:
        return self._id_pengguna

    def tampilkan_profil(self):
        print(f"\n{'='*40}")
        print(f"  ID       : {self._id_pengguna}")
        print(f"  Nama     : {self._nama}")
        print(f"  Email    : {self._email}")
        print(f"  Telepon  : {self._telepon}")
        print(f"  Role     : {self.__class__.__name__}")
        print(f"{'='*40}")


# ============================================================
# SECTION 2: KELAS TURUNAN - ADMIN
# Konsep: INHERITANCE (mewarisi Pengguna)
# ============================================================

class Admin(Pengguna):
    """
    Turunan dari Pengguna.
    Admin memiliki hak tambah/hapus/ubah jadwal penerbangan.
    """

    def __init__(self, nama: str, email: str, telepon: str, kode_admin: str):
        super().__init__(nama, email, telepon)  # Memanggil konstruktor induk
        self.__kode_admin = kode_admin           # Private (__)

    def tambah_penerbangan(self, sistem, kode: str, asal: str, tujuan: str,
                           jadwal: str, kapasitas: int, harga_dasar: float):
        """Admin menambahkan jadwal penerbangan baru ke sistem."""
        penerbangan = Penerbangan(kode, asal, tujuan, jadwal, kapasitas, harga_dasar)
        sistem.daftar_penerbangan[kode] = penerbangan
        print(f"\n[✓] Penerbangan {kode} ({asal} → {tujuan}) berhasil ditambahkan.")
        return penerbangan

    def hapus_penerbangan(self, sistem, kode: str):
        """Admin menghapus jadwal penerbangan dari sistem."""
        if kode in sistem.daftar_penerbangan:
            del sistem.daftar_penerbangan[kode]
            print(f"\n[✓] Penerbangan {kode} berhasil dihapus.")
        else:
            print(f"\n[✗] Penerbangan {kode} tidak ditemukan.")

    def lihat_semua_penerbangan(self, sistem):
        """Admin melihat seluruh daftar penerbangan."""
        sistem.tampilkan_semua_penerbangan()

    def verifikasi_admin(self, kode: str) -> bool:
        return self.__kode_admin == kode


# ============================================================
# SECTION 3: KELAS TURUNAN - PENUMPANG
# Konsep: INHERITANCE (mewarisi Pengguna)
# ============================================================

class Penumpang(Pengguna):
    """
    Turunan dari Pengguna.
    Penumpang dapat memesan tiket dan melihat riwayat pemesanan.
    """

    def __init__(self, nama: str, email: str, telepon: str, nomor_paspor: str):
        super().__init__(nama, email, telepon)
        self._nomor_paspor = nomor_paspor
        self.__riwayat_pemesanan = []  # Private list tiket

    def pesan_tiket(self, penerbangan, kelas_tiket: str, nomor_kursi: str = None) -> 'Tiket | None':
        """Penumpang memesan kursi pada penerbangan tertentu."""
        kursi = penerbangan.pesan_kursi(self, kelas_tiket, nomor_kursi)
        if kursi:
            # Buat objek tiket sesuai kelas
            if kelas_tiket.lower() == "bisnis":
                tiket = TiketBisnis(self, penerbangan, kursi)
            else:
                tiket = TiketEkonomi(self, penerbangan, kursi)

            self.__riwayat_pemesanan.append(tiket)
            tiket.cetak_tiket()
            return tiket
        return None

    def riwayat_pemesanan(self):
        """Penumpang melihat semua tiket yang pernah dipesan."""
        if not self.__riwayat_pemesanan:
            print(f"\n[i] {self._nama} belum memiliki riwayat pemesanan.")
            return
        print(f"\n{'='*50}")
        print(f"  RIWAYAT PEMESANAN - {self._nama}")
        print(f"{'='*50}")
        for i, tiket in enumerate(self.__riwayat_pemesanan, 1):
            print(f"\n[{i}] Kode Tiket : {tiket.get_kode_tiket()}")
            print(f"    Rute      : {tiket.penerbangan.asal} → {tiket.penerbangan.tujuan}")
            print(f"    Kursi     : {tiket.nomor_kursi}")
            kelas = getattr(tiket, '_kelas', tiket.__class__.__name__)
            print(f"    Kelas     : {kelas}")
            print(f"    Harga     : Rp {tiket.hitung_harga_akhir():,.0f}")


# ============================================================
# SECTION 4: KELAS PENERBANGAN
# Konsep: ENCAPSULATION — kursi dikelola via metode, bukan akses langsung
# ============================================================

class Penerbangan:
    """
    Merepresentasikan satu jadwal penerbangan.
    Konsep OOP: Encapsulation — _daftar_penumpang_terdaftar adalah protected,
                kursi hanya bisa dipesan via metode pesan_kursi()
    """

    def __init__(self, kode: str, asal: str, tujuan: str,
                 jadwal: str, kapasitas: int, harga_dasar: float):
        self.kode = kode
        self.asal = asal
        self.tujuan = tujuan
        self.jadwal = jadwal
        self.harga_dasar = harga_dasar
        self._kapasitas = kapasitas

        # Protected — tidak boleh diakses/diubah sembarangan dari luar
        self._daftar_penumpang_terdaftar = {}  # {nomor_kursi: Penumpang}
        self._status_kursi = {}                 # {nomor_kursi: 'tersedia'/'terpesan'}

        # Inisialisasi semua kursi sebagai tersedia
        self.__inisialisasi_kursi()

    def __inisialisasi_kursi(self):
        """Private method — hanya dipanggil saat objek dibuat."""
        # Baris A-F untuk ekonomi, 1 sampai kapasitas
        for nomor in range(1, self._kapasitas + 1):
            for huruf in ['A', 'B', 'C', 'D', 'E', 'F']:
                kode_kursi = f"{nomor}{huruf}"
                self._status_kursi[kode_kursi] = 'tersedia'

    def tampilkan_kursi(self):
        """Menampilkan denah kursi (tersedia/terpesan) dalam bentuk grid."""
        print(f"\n  Denah Kursi Penerbangan {self.kode}:")
        print(f"  {'─'*35}")
        for nomor in range(1, self._kapasitas + 1):
            baris = "  "
            for huruf in ['A', 'B', 'C', 'D', 'E', 'F']:
                kode = f"{nomor}{huruf}"
                if self._status_kursi.get(kode) == 'tersedia':
                    baris += f"[{kode}] "
                else:
                    baris += f"[XX]  "
            print(baris)
            if nomor % 2 == 0:
                print()
        print(f"  [XX] = Terisi  |  [1A] = Tersedia")
        print(f"  {'─'*35}")

    def pesan_kursi(self, penumpang: Penumpang, kelas_tiket: str, nomor_kursi: str = None) -> str | None:
        """
        Memesan kursi tertentu (atau otomatis jika tidak ditentukan).
        """
        if nomor_kursi:
            if nomor_kursi not in self._status_kursi:
                print(f"\n[✗] Kursi {nomor_kursi} tidak valid.")
                return None
            if self._status_kursi[nomor_kursi] != 'tersedia':
                print(f"\n[✗] Kursi {nomor_kursi} sudah dipesan orang lain!")
                return None
            self._status_kursi[nomor_kursi] = 'terpesan'
            self._daftar_penumpang_terdaftar[nomor_kursi] = penumpang
            print(f"\n[✓] Kursi {nomor_kursi} berhasil dipesan untuk {penumpang.get_nama()}.")
            return nomor_kursi

        for nomor_kursi, status in self._status_kursi.items():
            if status == 'tersedia':
                self._status_kursi[nomor_kursi] = 'terpesan'
                self._daftar_penumpang_terdaftar[nomor_kursi] = penumpang
                print(f"\n[✓] Kursi {nomor_kursi} berhasil dipesan untuk {penumpang.get_nama()}.")
                return nomor_kursi

        print(f"\n[✗] Maaf, tidak ada kursi tersedia di penerbangan {self.kode}.")
        return None

    def cek_kursi_tersedia(self) -> int:
        """Mengembalikan jumlah kursi yang masih tersedia."""
        return sum(1 for s in self._status_kursi.values() if s == 'tersedia')

    def tampilkan_info(self):
        print(f"\n  Kode       : {self.kode}")
        print(f"  Rute       : {self.asal} → {self.tujuan}")
        print(f"  Jadwal     : {self.jadwal}")
        print(f"  Harga Dasar: Rp {self.harga_dasar:,.0f}")
        print(f"  Kursi Sisa : {self.cek_kursi_tersedia()} dari {self._kapasitas * 6}")


# ============================================================
# SECTION 5: KELAS TIKET (BASE CLASS)
# Konsep: POLYMORPHISM — hitung_harga_akhir() di-override tiap subclass
# ============================================================

class KelasTiket:
    """
    Kelas dasar untuk semua jenis tiket.
    Konsep OOP: Polymorphism — metode hitung_harga_akhir() akan berperilaku
                berbeda di TiketEkonomi vs TiketBisnis.
    """

    def __init__(self, penumpang: Penumpang, penerbangan: Penerbangan, nomor_kursi: str):
        self.penumpang = penumpang
        self.penerbangan = penerbangan
        self.nomor_kursi = nomor_kursi
        self.__kode_tiket = "TKT-" + str(uuid.uuid4())[:6].upper()
        self.waktu_pesan = datetime.datetime.now().strftime("%d/%m/%Y %H:%M")

    def get_kode_tiket(self) -> str:
        return self.__kode_tiket

    def hitung_harga_akhir(self) -> float:
        """
        Metode yang di-override oleh subclass (Polymorphism).
        Kelas dasar hanya mengembalikan harga dasar.
        """
        return self.penerbangan.harga_dasar

    def cetak_tiket(self):
        harga = self.hitung_harga_akhir()  # Polymorphism bekerja di sini
        print(f"\n{'='*55}")
        print(f"  ✈  E-TICKET PESAWAT  ✈")
        print(f"{'='*55}")
        print(f"  Kode Tiket  : {self.__kode_tiket}")
        print(f"  Penumpang   : {self.penumpang.get_nama()}")
        print(f"  Email       : {self.penumpang.get_email()}")
        print(f"  Penerbangan : {self.penerbangan.kode}")
        print(f"  Rute        : {self.penerbangan.asal} → {self.penerbangan.tujuan}")
        print(f"  Jadwal      : {self.penerbangan.jadwal}")
        print(f"  Kursi       : {self.nomor_kursi}")
        print(f"  Kelas       : {self.__class__.__name__}")
        print(f"  Dipesan     : {self.waktu_pesan}")
        print(f"  {'─'*51}")
        print(f"  Harga Akhir : Rp {harga:,.0f}")
        print(f"{'='*55}")
        print(f"  Status Kursi: [TERPESAN ✓]")
        print(f"{'='*55}")


# ============================================================
# SECTION 6: KELAS TIKET EKONOMI
# Konsep: POLYMORPHISM — override hitung_harga_akhir()
# ============================================================

class TiketEkonomi(KelasTiket):
    """
    Tiket kelas Ekonomi.
    Polymorphism: hitung_harga_akhir() = harga_dasar + pajak_standar (10%)
    """
    PAJAK_PERSEN = 0.10
    BIAYA_ADMIN  = 25_000

    def hitung_harga_akhir(self) -> float:
        """Override — tambahkan pajak standar dan biaya admin."""
        harga_dasar = self.penerbangan.harga_dasar
        pajak = harga_dasar * self.PAJAK_PERSEN
        return harga_dasar + pajak + self.BIAYA_ADMIN

    def cetak_rincian_harga(self):
        harga_dasar = self.penerbangan.harga_dasar
        pajak = harga_dasar * self.PAJAK_PERSEN
        print(f"\n  Rincian Harga (Ekonomi):")
        print(f"    Harga Dasar  : Rp {harga_dasar:,.0f}")
        print(f"    Pajak (10%)  : Rp {pajak:,.0f}")
        print(f"    Biaya Admin  : Rp {self.BIAYA_ADMIN:,.0f}")
        print(f"    Total        : Rp {self.hitung_harga_akhir():,.0f}")


# ============================================================
# SECTION 7: KELAS TIKET BISNIS
# Konsep: POLYMORPHISM — override hitung_harga_akhir()
# ============================================================

class TiketBisnis(KelasTiket):
    """
    Tiket kelas Bisnis.
    Polymorphism: hitung_harga_akhir() = harga_dasar * 2.5 + fasilitas_extra
    """
    MULTIPLIER_BISNIS  = 2.5
    BIAYA_LOUNGE       = 150_000
    BIAYA_BAGASI_EXTRA = 200_000

    def hitung_harga_akhir(self) -> float:
        """
        Override — harga dikalikan 2.5 dan ditambah fasilitas eksklusif.
        Metode yang sama, perilaku yang BERBEDA (Polymorphism).
        """
        harga_dasar = self.penerbangan.harga_dasar
        harga_bisnis = harga_dasar * self.MULTIPLIER_BISNIS
        return harga_bisnis + self.BIAYA_LOUNGE + self.BIAYA_BAGASI_EXTRA

    def cetak_rincian_harga(self):
        harga_dasar = self.penerbangan.harga_dasar
        harga_bisnis = harga_dasar * self.MULTIPLIER_BISNIS
        print(f"\n  Rincian Harga (Bisnis):")
        print(f"    Harga Dasar    : Rp {harga_dasar:,.0f}")
        print(f"    Tarif Bisnis x2.5 : Rp {harga_bisnis:,.0f}")
        print(f"    Akses Lounge   : Rp {self.BIAYA_LOUNGE:,.0f}")
        print(f"    Bagasi Extra   : Rp {self.BIAYA_BAGASI_EXTRA:,.0f}")
        print(f"    Total          : Rp {self.hitung_harga_akhir():,.0f}")


# ============================================================
# SECTION 8: SISTEM UTAMA (CONTROLLER)
# ============================================================

class TiketTersimpan:
    def __init__(self, info):
        self.__kode_tiket = info[0]
        self.penerbangan = lambda: None
        self.penerbangan.kode = info[1]
        self.nomor_kursi = info[2]
        self._kelas = info[3]
        self.waktu_pesan = info[4]
        self.__harga = int(info[5])
        self.penerbangan.asal = info[6]
        self.penerbangan.tujuan = info[7]

    def get_kode_tiket(self):
        return self.__kode_tiket

    def hitung_harga_akhir(self):
        return self.__harga


DATA_FILE = "data_reservasi.txt"


class SistemReservasi:
    """
    Kelas controller — mengelola seluruh data penerbangan dan pengguna.
    """

    def __init__(self):
        self.daftar_penerbangan = {}  # {kode: Penerbangan}
        self.daftar_pengguna = {}     # {id: Pengguna}

    def simpan_data(self, id_aktif=None):
        with open(DATA_FILE, "w") as f:
            if id_aktif:
                f.write(f"AKTIF|{id_aktif}\n")
            for pid, p in self.daftar_pengguna.items():
                if isinstance(p, Penumpang):
                    f.write(f"P|{p._id_pengguna}|{p._nama}|{p._email}|{p._telepon}|{p._nomor_paspor}\n")
                    for t in p._Penumpang__riwayat_pemesanan:
                        kelas = getattr(t, '_kelas', t.__class__.__name__)
                        f.write(f"T|{p._id_pengguna}|{t.get_kode_tiket()}|{t.penerbangan.kode}|"
                                f"{t.nomor_kursi}|{kelas}|{t.waktu_pesan}|"
                                f"{int(t.hitung_harga_akhir())}|{t.penerbangan.asal}|{t.penerbangan.tujuan}\n")
            for kode, pnb in self.daftar_penerbangan.items():
                for kursi, status in pnb._status_kursi.items():
                    f.write(f"S|{kode}|{kursi}|{status}\n")

    def muat_data(self):
        if not os.path.exists(DATA_FILE):
            return None
        id_aktif = None
        with open(DATA_FILE) as f:
            for baris in f:
                baris = baris.strip()
                if not baris:
                    continue
                parts = baris.split("|")
                if parts[0] == "AKTIF":
                    id_aktif = parts[1]
                elif parts[0] == "P":
                    p = Penumpang(parts[2], parts[3], parts[4], parts[5])
                    p._id_pengguna = parts[1]
                    self.daftar_pengguna[parts[1]] = p
                elif parts[0] == "T":
                    pid = parts[1]
                    if pid in self.daftar_pengguna:
                        t = TiketTersimpan(parts[2:])
                        self.daftar_pengguna[pid]._Penumpang__riwayat_pemesanan.append(t)
                elif parts[0] == "S":
                    if parts[1] in self.daftar_penerbangan:
                        self.daftar_penerbangan[parts[1]]._status_kursi[parts[2]] = parts[3]
        return id_aktif

    def tampilkan_semua_penerbangan(self):
        if not self.daftar_penerbangan:
            print("\n[i] Tidak ada jadwal penerbangan tersedia.")
            return
        print(f"\n{'='*55}")
        print(f"  DAFTAR JADWAL PENERBANGAN TERSEDIA")
        print(f"{'='*55}")
        for kode, pnb in self.daftar_penerbangan.items():
            pnb.tampilkan_info()
            print(f"  {'─'*51}")

    def cari_penerbangan(self, tujuan: str):
        hasil = [p for p in self.daftar_penerbangan.values()
                 if tujuan.lower() in p.tujuan.lower()]
        if not hasil:
            print(f"\n[✗] Tidak ada penerbangan ke '{tujuan}'.")
            return []
        print(f"\n[✓] Ditemukan {len(hasil)} penerbangan ke '{tujuan}':")
        for p in hasil:
            p.tampilkan_info()
            print()
        return hasil

    def daftarkan_pengguna(self, pengguna: Pengguna):
        self.daftar_pengguna[pengguna.get_id()] = pengguna
        print(f"[✓] Pengguna '{pengguna.get_nama()}' ({pengguna.__class__.__name__}) berhasil didaftarkan.")


# ============================================================
# SECTION 9: DEMONSTRASI PROGRAM (MAIN)
# ============================================================

def main():
    sistem = SistemReservasi()
    penumpang = None

    admin = Admin("Admin", "admin@airline.com", "081234567890", "ADMIN123")
    sistem.daftarkan_pengguna(admin)
    admin.tambah_penerbangan(sistem, "GA-101", "Jakarta (CGK)", "Surabaya (SUB)", "2025-07-10 08:00", 10, 750_000)
    admin.tambah_penerbangan(sistem, "JT-202", "Jakarta (CGK)", "Bali (DPS)", "2025-07-12 14:00", 10, 1_200_000)
    admin.tambah_penerbangan(sistem, "ID-303", "Surabaya (SUB)", "Makassar (UPG)", "2025-07-15 10:30", 5, 900_000)

    aktif_id = sistem.muat_data()
    if aktif_id and aktif_id in sistem.daftar_pengguna:
        penumpang = sistem.daftar_pengguna[aktif_id]
        print(f"\n[✓] Selamat datang kembali, {penumpang.get_nama()}!")

    while True:
        print(f"\n{'='*55}")
        print("  MENU UTAMA")
        print(f"{'='*55}")
        print("  1. Daftarkan diri (isi data diri)")
        print("  2. Lihat semua jadwal penerbangan")
        print("  3. Pesan tiket")
        print("  4. Lihat riwayat pemesanan")
        print("  5. Demo Polymorphism")
        print("  0. Keluar")
        print(f"{'='*55}")

        pilihan = input("Pilih menu: ").strip()

        if pilihan == "1":
            print(f"\n{'='*50}")
            print("  REGISTRASI PENUMPANG")
            print(f"{'='*50}")
            nama = input("  Nama\t\t: ").strip()
            email = input("  Email\t\t: ").strip()
            telepon = input("  Telepon\t: ").strip()
            paspor = input("  No. Paspor\t: ").strip()
            penumpang = Penumpang(nama, email, telepon, paspor)
            sistem.daftarkan_pengguna(penumpang)
            penumpang.tampilkan_profil()
            sistem.simpan_data(penumpang.get_id())

        elif pilihan == "2":
            sistem.tampilkan_semua_penerbangan()

        elif pilihan == "3":
            if not penumpang:
                print("\n  [✗] Kamu belum daftar! Pilih menu 1 dulu.")
                continue
            if not sistem.daftar_penerbangan:
                print("\n  [✗] Tidak ada penerbangan tersedia.")
                continue

            sistem.tampilkan_semua_penerbangan()
            kode = input("\n  Masukkan kode penerbangan: ").strip().upper()
            if kode not in sistem.daftar_penerbangan:
                print(f"\n  [✗] Kode '{kode}' tidak ditemukan.")
                continue

            print("  Kelas: (e) Ekonomi / (b) Bisnis")
            kelas = input("  Pilih kelas: ").strip().lower()
            if kelas == "b":
                kelas_tiket = "bisnis"
            else:
                kelas_tiket = "ekonomi"

            penerbangan = sistem.daftar_penerbangan[kode]
            penerbangan.tampilkan_kursi()
            kursi = input("  Masukkan nomor kursi (misal 1A) atau Enter untuk otomatis: ").strip().upper()

            print(f"\n  → {penumpang.get_nama()} memesan Tiket {kelas_tiket.upper()} ke {penerbangan.tujuan}:")
            penumpang.pesan_tiket(penerbangan, kelas_tiket, kursi if kursi else None)
            sistem.simpan_data(penumpang.get_id())

        elif pilihan == "4":
            if not penumpang:
                print("\n  [✗] Kamu belum daftar! Pilih menu 1 dulu.")
                continue
            penumpang.riwayat_pemesanan()

        elif pilihan == "5":
            if not sistem.daftar_penerbangan:
                print("\n  [✗] Tidak ada penerbangan.")
                continue
            kode = list(sistem.daftar_penerbangan.keys())[0]
            pnb = sistem.daftar_penerbangan[kode]

            print(f"\n{'='*55}")
            print(f"  DEMO POLYMORPHISM — hitung_harga_akhir()")
            print(f"  Penerbangan: {pnb.kode}")
            print(f"{'='*55}")
            print("  Metode SAMA, hasil BERBEDA:\n")

            dummy = Penumpang("Demo", "demo@test.com", "0", "X999")
            for tiket in [TiketEkonomi(dummy, pnb, "10A"), TiketBisnis(dummy, pnb, "1A")]:
                print(f"  [{tiket.__class__.__name__}]")
                tiket.cetak_rincian_harga()
                print()

        elif pilihan == "0":
            sistem.simpan_data(penumpang.get_id() if penumpang else None)
            print("\n  Terima kasih telah menggunakan sistem reservasi!")
            print(f"  Konsep OOP yang telah didemonstrasikan:")
            print(f"  1. Encapsulation : Atribut protected/private")
            print(f"  2. Inheritance   : Admin & Penumpang ← Pengguna")
            print(f"  3. Polymorphism  : hitung_harga_akhir()")
            break

        else:
            print("\n  [✗] Pilihan tidak valid. Coba lagi.")


if __name__ == "__main__":
    main()