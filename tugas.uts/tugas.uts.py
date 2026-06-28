"""
=============================================================
  SISTEM RESERVASI TIKET PESAWAT
  Study Case: Object-Oriented Programming (OOP) in Python
  By: Tamam Ni'amillah Ramdhan Putra Widyana (462025611095)
  University of Darussalam Gontor - 2025/2026
=============================================================

Konsep OOP yang Diterapkan:
  1. Encapsulation  → Melindungi data internal (atribut private/protected)
  2. Inheritance    → Pewarisan kelas Pengguna → Admin & Penumpang
  3. Polymorphism   → Metode hitung_harga_akhir() berbeda tiap jenis tiket
"""

import uuid
import datetime


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

    def pesan_tiket(self, penerbangan, kelas_tiket: str) -> 'Tiket | None':
        """Penumpang memesan kursi pada penerbangan tertentu."""
        kursi = penerbangan.pesan_kursi(self, kelas_tiket)
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
            print(f"    Kelas     : {tiket.__class__.__name__}")
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

    def pesan_kursi(self, penumpang: Penumpang, kelas_tiket: str) -> str | None:
        """
        Metode utama pemesanan kursi.
        Encapsulation: Validasi dilakukan di dalam — tidak bisa di-bypass dari luar.
        Mengembalikan nomor kursi jika berhasil, None jika gagal.
        """
        # Cari kursi tersedia pertama
        for nomor_kursi, status in self._status_kursi.items():
            if status == 'tersedia':
                # Validasi berhasil → ubah status
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

class SistemReservasi:
    """
    Kelas controller — mengelola seluruh data penerbangan dan pengguna.
    """

    def __init__(self):
        self.daftar_penerbangan = {}  # {kode: Penerbangan}
        self.daftar_pengguna = {}     # {id: Pengguna}

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

def demo_polymorphism(penerbangan: Penerbangan):
    """
    Demo eksplisit Polymorphism:
    Memanggil hitung_harga_akhir() dari dua objek bertipe berbeda.
    Sistem tidak perlu tahu detailnya — polimorfisme menangani sendiri.
    """
    print(f"\n{'='*55}")
    print(f"  DEMO POLYMORPHISM — hitung_harga_akhir()")
    print(f"  Penerbangan: {penerbangan.kode}")
    print(f"{'='*55}")
    print("  Sistem cukup memanggil SATU metode yang sama,")
    print("  tapi hasilnya BERBEDA untuk tiap kelas tiket:\n")

    penumpang_dummy = Penumpang("Demo User", "demo@test.com", "08000000", "X999")
    tiket_list = [
        TiketEkonomi(penumpang_dummy, penerbangan, "10A"),
        TiketBisnis(penumpang_dummy, penerbangan, "1A"),
    ]

    for tiket in tiket_list:
        # Polymorphism: sama-sama dipanggil hitung_harga_akhir(),
        # tapi logikanya berbeda tergantung tipe objek nyatanya
        print(f"  [{tiket.__class__.__name__}]")
        tiket.cetak_rincian_harga()
        print()


def main():
    print("\n" + "=" * 60)
    print("   SISTEM RESERVASI TIKET PESAWAT")
    print("   OOP Study Case — Tamam Ni'amillah (462025611095)")
    print("   University of Darussalam Gontor 2025/2026")
    print("=" * 60)

    # --------------------------------------------------
    # 1. Inisialisasi Sistem
    # --------------------------------------------------
    sistem = SistemReservasi()

    # --------------------------------------------------
    # 2. Buat Admin (Inheritance: Admin ← Pengguna)
    # --------------------------------------------------
    print("\n[TAHAP 1] Membuat Admin & Mendaftarkan Pengguna")
    print("-" * 50)
    admin = Admin(
        nama="Budi Santoso",
        email="budi.admin@airline.com",
        telepon="081234567890",
        kode_admin="ADMIN123"
    )
    sistem.daftarkan_pengguna(admin)
    admin.tampilkan_profil()

    # --------------------------------------------------
    # 3. Admin menambahkan jadwal penerbangan
    # --------------------------------------------------
    print("\n[TAHAP 2] Admin Menambahkan Jadwal Penerbangan")
    print("-" * 50)
    admin.tambah_penerbangan(
        sistem,
        kode="GA-101",
        asal="Jakarta (CGK)",
        tujuan="Surabaya (SUB)",
        jadwal="2025-07-10 08:00",
        kapasitas=10,
        harga_dasar=750_000
    )
    admin.tambah_penerbangan(
        sistem,
        kode="JT-202",
        asal="Jakarta (CGK)",
        tujuan="Bali (DPS)",
        jadwal="2025-07-12 14:00",
        kapasitas=10,
        harga_dasar=1_200_000
    )
    admin.tambah_penerbangan(
        sistem,
        kode="ID-303",
        asal="Surabaya (SUB)",
        tujuan="Makassar (UPG)",
        jadwal="2025-07-15 10:30",
        kapasitas=5,
        harga_dasar=900_000
    )

    # --------------------------------------------------
    # 4. Tampilkan semua penerbangan
    # --------------------------------------------------
    print("\n[TAHAP 3] Menampilkan Semua Jadwal Penerbangan")
    print("-" * 50)
    admin.lihat_semua_penerbangan(sistem)

    # --------------------------------------------------
    # 5. Buat Penumpang (Inheritance: Penumpang ← Pengguna)
    # --------------------------------------------------
    print("\n[TAHAP 4] Mendaftarkan Penumpang")
    print("-" * 50)
    penumpang1 = Penumpang(
        nama="Siti Rahayu",
        email="siti@gmail.com",
        telepon="082345678901",
        nomor_paspor="A1234567"
    )
    penumpang2 = Penumpang(
        nama="Ahmad Fauzi",
        email="fauzi@gmail.com",
        telepon="083456789012",
        nomor_paspor="B9876543"
    )
    sistem.daftarkan_pengguna(penumpang1)
    sistem.daftarkan_pengguna(penumpang2)
    penumpang1.tampilkan_profil()
    penumpang2.tampilkan_profil()

    # --------------------------------------------------
    # 6. Pencarian penerbangan
    # --------------------------------------------------
    print("\n[TAHAP 5] Penumpang Mencari Penerbangan ke Bali")
    print("-" * 50)
    sistem.cari_penerbangan("Bali")

    # --------------------------------------------------
    # 7. Pemesanan Tiket (Encapsulation + Polymorphism)
    # --------------------------------------------------
    print("\n[TAHAP 6] Pemesanan Tiket")
    print("-" * 50)

    # Penumpang 1: pesan kelas Ekonomi ke Bali
    penerbangan_bali = sistem.daftar_penerbangan["JT-202"]
    print(f"\n→ {penumpang1.get_nama()} memesan Tiket EKONOMI ke Bali:")
    penumpang1.pesan_tiket(penerbangan_bali, "ekonomi")

    # Penumpang 2: pesan kelas Bisnis ke Bali
    print(f"\n→ {penumpang2.get_nama()} memesan Tiket BISNIS ke Bali:")
    penumpang2.pesan_tiket(penerbangan_bali, "bisnis")

    # Penumpang 1: pesan lagi ke Surabaya
    penerbangan_sby = sistem.daftar_penerbangan["GA-101"]
    print(f"\n→ {penumpang1.get_nama()} memesan Tiket EKONOMI ke Surabaya:")
    penumpang1.pesan_tiket(penerbangan_sby, "ekonomi")

    # --------------------------------------------------
    # 8. Lihat Riwayat Pemesanan (Encapsulation: private list)
    # --------------------------------------------------
    print("\n[TAHAP 7] Melihat Riwayat Pemesanan")
    print("-" * 50)
    penumpang1.riwayat_pemesanan()
    penumpang2.riwayat_pemesanan()

    # --------------------------------------------------
    # 9. Demo eksplisit Polymorphism
    # --------------------------------------------------
    print("\n[TAHAP 8] Demo Eksplisit POLYMORPHISM")
    print("-" * 50)
    demo_polymorphism(penerbangan_bali)

    # --------------------------------------------------
    # 10. Sisa kursi setelah pemesanan (Encapsulation)
    # --------------------------------------------------
    print("\n[TAHAP 9] Cek Sisa Kursi (Encapsulation)")
    print("-" * 50)
    print(f"  Penerbangan {penerbangan_bali.kode}: "
          f"{penerbangan_bali.cek_kursi_tersedia()} kursi tersisa")
    print(f"  Penerbangan {penerbangan_sby.kode}: "
          f"{penerbangan_sby.cek_kursi_tersedia()} kursi tersisa")

    # --------------------------------------------------
    # 11. Admin hapus penerbangan
    # --------------------------------------------------
    print("\n[TAHAP 10] Admin Menghapus Penerbangan ID-303")
    print("-" * 50)
    admin.hapus_penerbangan(sistem, "ID-303")
    admin.lihat_semua_penerbangan(sistem)

    print("\n" + "=" * 60)
    print("  PROGRAM SELESAI — Semua konsep OOP berhasil didemonstrasikan")
    print("  1. Encapsulation : Atribut protected/private + akses via metode")
    print("  2. Inheritance   : Admin & Penumpang mewarisi kelas Pengguna")
    print("  3. Polymorphism  : hitung_harga_akhir() berbeda tiap jenis tiket")
    print("=" * 60)


if __name__ == "__main__":
    main()