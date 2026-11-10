# 📷 Aplikasi Kamera Infrared & Thermal Vision

Aplikasi pemrosesan citra kamera inframerah & termal realtime dengan antarmuka HUD taktis futuristik. Tersedia dalam versi **Web / Mobile Browser (WebGL)** dan **Python (OpenCV)**.

---

## 🌟 Fitur Utama

1. **6 Mode Palet Spektral Inframerah & Termal:**
   - **Ironbow (FLIR Standard):** Gradien ungu-merah-kuning-putih standar kamera termal industri.
   - **Rainbow / Jet:** Spektrum pelangi dinamis untuk kontras gradien suhu tinggi.
   - **Inferno:** Visualisasi peta panas radiasi intens.
   - **Night Vision (Green Phosphor):** Simulasi inframerah malam militer lengkap dengan efek *digital sensor grain* dan *scanline*.
   - **Classic IR (Wood Effect):** Simulasi fotografi inframerah dekat (Near-IR 720nm-850nm), di mana daun/klorofil tampak putih berkilau dan langit menggelap.
   - **MSX Edge Thermal Fusion:** Teknologi fusi kontur seperti pada kamera FLIR MSX (deteksi tepi objek digabungkan ke peta termal).

2. **Deteksi & Pelacakan Titik Panas (Hotspot Tracking):**
   - Crosshair bidik tengah dengan estimasi temperatur target (°C).
   - Marker otomatis yang melacak titik paling panas pada frame secara realtime.
   - Bar skala suhu termal dinamis di sisi kanan layar.

3. **Kontrol Kamera Penuh:**
   - Slider **Sensitivity / Gain** dan **Contrast** dinamis.
   - Tombol beralih kamera (Kamera Belakang / Kamera Depan).
   - Kontrol lampu senter / flash kamera (jika didukung perangkat).
   - Tombol **Shutter Snapshot** dengan efek animasi kilat untuk menyimpan foto langsung ke galeri.

---

## 🚀 Cara Menjalankan

### Cara 1: Menggunakan Web Browser (Paling Direkomendasikan untuk HP Android)

Aplikasi Web menggunakan WebGL Shaders terakselerasi GPU sehingga berjalan sangat lancar (60 FPS) langsung di HP Anda.

1. Jalankan server lokal dengan Python:
   ```bash
   python /data/user/0/com.agy/files/.gemini/antigravity-app/scratch/infrared-camera/server.py
   ```
2. Buka browser (Chrome / Antigravity Webview) dan akses:
   ```
   http://localhost:8080
   ```
3. Izinkan akses kamera saat diminta.

*(Catatan: Anda juga bisa membuka file [index.html](file:///data/user/0/com.agy/files/.gemini/antigravity-app/scratch/infrared-camera/index.html) secara langsung).*

---

### Cara 2: Menggunakan Python + OpenCV (Untuk Laptop / Terminal / USB WebCam)

Jika Anda menghubungkan kamera USB atau webcam eksternal:

```bash
python /data/user/0/com.agy/files/.gemini/antigravity-app/scratch/infrared-camera/app.py
```

**Kontrol Keyboard:**
- `0` - `4` : Ganti mode palet
- `+` / `-` : Atur gain / sensitivitas
- `s` : Ambil screenshot / foto
- `q` : Keluar

---

## 🔬 Catatan Teknis tentang Kamera Infrared pada Smartphone

- **Sensor Bawaan HP:** Kamera ponsel standar memiliki filter fisik internal (**IR-Cut Filter**) yang sengaja memblokir sinar inframerah agar foto normal tidak terdistorsi warna kemerahan.
- **Kamera Termal Fisik Asli (LWIR 8–14 µm):** Memerlukan sensor *microbolometer* terpisah (seperti dongle FLIR ONE, Seek Thermal, atau Infiray USB).
- **Simulasi Spektral / Pseudo-Coloring:** Aplikasi ini mengonversi densitas luminansi, kontras spektral RGB, dan algoritma *Sobel edge detection* ke dalam LUT (*Look-Up Table*) warna termal standar industri untuk menghasilkan efek visual inframerah yang akurat dan responsif.
