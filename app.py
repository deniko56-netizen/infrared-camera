"""
Aplikasi Kamera Infrared & Thermal Vision (Python + OpenCV)
Mendukung feed kamera realtime, pemilihan palet (Ironbow, Rainbow, Inferno, Night Vision, Edge Fusion),
serta pelacakan titik panas (hotspot detection).
"""

import cv2
import numpy as np
import time

def apply_ironbow_palette(gray):
    """
    Simulasi palet Ironbow FLIR menggunakan ColorMap bawaan atau custom LUT
    """
    # COLORMAP_INFERNO atau COLORMAP_MAGMA memberikan efek visual mirip Ironbow FLIR
    return cv2.applyColorMap(gray, cv2.COLORMAP_INFERNO)

def apply_night_vision(frame):
    """
    Simulasi Night Vision Inframerah (Green Phosphor + Noise)
    """
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    # Tambahkan sedikit noise digital
    noise = np.random.normal(0, 8, gray.shape).astype(np.uint8)
    enhanced = cv2.add(gray, noise)
    
    # Buat kanal hijau dominan
    h, w = gray.shape
    green_img = np.zeros((h, w, 3), dtype=np.uint8)
    green_img[:, :, 1] = cv2.equalizeHist(enhanced) # Green channel
    green_img[:, :, 0] = (enhanced * 0.2).astype(np.uint8) # Sedikit biru
    return green_img

def apply_wood_effect_ir(frame):
    """
    Simulasi Efek Wood Inframerah Dekat (B&W IR):
    Klorofil/daun memantulkan IR (menjadi putih terang), langit menjadi gelap.
    """
    b, g, r = cv2.split(frame)
    # Rumus aproksimasi reflektansi IR dari saluran RGB
    ir_sim = (0.6 * r.astype(np.float32) + 0.5 * g.astype(np.float32) - 0.2 * b.astype(np.float32))
    ir_sim = np.clip(ir_sim, 0, 255).astype(np.uint8)
    # Tingkatkan kontras
    clahe = cv2.createCLAHE(clipLimit=2.0, tileGridSize=(8,8))
    ir_enhanced = clahe.apply(ir_sim)
    return cv2.cvtColor(ir_enhanced, cv2.COLOR_GRAY2BGR)

def apply_msx_edge_fusion(frame, thermal_colored):
    """
    Simulasi FLIR MSX (Thermal + Edge Detection Overlay)
    """
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    edges = cv2.Canny(gray, 50, 150)
    edges_colored = cv2.cvtColor(edges, cv2.COLOR_GRAY2BGR)
    # Gabungkan garis tepi putih ke atas peta termal
    fused = cv2.addWeighted(thermal_colored, 0.85, edges_colored, 0.4, 0)
    return fused

def main():
    cap = cv2.VideoCapture(0)
    if not cap.isOpened():
        print("Peringatan: Kamera tidak dapat diakses atau tidak ditemukan.")
        print("Jika di Android, gunakan versi Web (index.html) melalui browser.")
        return

    mode = 0
    modes = ["IRONBOW (FLIR)", "RAINBOW / JET", "NIGHT VISION", "CLASSIC IR (WOOD EFFECT)", "MSX EDGE FUSION"]
    
    gain = 1.2
    contrast = 1.3

    print("=== APLIKASI KAMERA INFRARED & THERMAL ===")
    print("Kontrol Keyboard:")
    print("  [0-4] : Ganti Mode Palet")
    print("  [+] / [-] : Naik / Turunkan Sensitivitas (Gain)")
    print("  [s]   : Ambil Foto (Screenshot)")
    print("  [q]   : Keluar")

    while True:
        ret, frame = cap.read()
        if not ret:
            break

        # Resize jika terlalu besar
        h, w = frame.shape[:2]
        if w > 800:
            frame = cv2.resize(frame, (800, int(h * 800 / w)))
            h, w = frame.shape[:2]

        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

        # Terapkan gain & kontras
        adjusted = cv2.convertScaleAbs(gray, alpha=gain, beta=(contrast - 1.0) * 20)

        # Pemrosesan palet
        if mode == 0:
            # Ironbow
            processed = apply_ironbow_palette(adjusted)
        elif mode == 1:
            # Rainbow
            processed = cv2.applyColorMap(adjusted, cv2.COLORMAP_JET)
        elif mode == 2:
            # Night Vision
            processed = apply_night_vision(frame)
        elif mode == 3:
            # Classic IR
            processed = apply_wood_effect_ir(frame)
        elif mode == 4:
            # MSX Edge Fusion
            base_thermal = apply_ironbow_palette(adjusted)
            processed = apply_msx_edge_fusion(frame, base_thermal)

        # Cari Hotspot (Titik paling panas/terang)
        min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(gray)
        simulated_max_temp = 24.0 + (max_val / 255.0) * 18.0 * (gain / 1.2)
        
        # Center temp
        center_val = gray[h // 2, w // 2]
        simulated_ctr_temp = 22.0 + (center_val / 255.0) * 16.0 * (gain / 1.2)

        # Render HUD Overlay
        # Crosshair tengah
        cv2.drawMarker(processed, (w // 2, h // 2), (0, 255, 204), markerType=cv2.MARKER_CROSS, markerSize=24, thickness=1)
        # Hotspot Marker
        cv2.circle(processed, max_loc, 10, (50, 50, 255), 2)
        cv2.putText(processed, f"MAX {simulated_max_temp:.1f}C", (max_loc[0] + 12, max_loc[1]),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.45, (50, 50, 255), 1, cv2.LINE_AA)

        # HUD Info bar
        cv2.putText(processed, f"MODE: {modes[mode]} | GAIN: {gain:.1f}x", (16, 30),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.55, (0, 255, 204), 1, cv2.LINE_AA)
        cv2.putText(processed, f"CTR: {simulated_ctr_temp:.1f}C", (w - 140, 30),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.55, (0, 255, 204), 1, cv2.LINE_AA)

        cv2.imshow("IR Thermal Camera Simulator", processed)

        key = cv2.waitKey(1) & 0xFF
        if key == ord('q'):
            break
        elif key in [ord('0'), ord('1'), ord('2'), ord('3'), ord('4')]:
            mode = int(chr(key))
        elif key == ord('+') or key == ord('='):
            gain = min(3.0, gain + 0.1)
        elif key == ord('-'):
            gain = max(0.5, gain - 0.1)
        elif key == ord('s'):
            filename = f"ir_snapshot_{int(time.time())}.png"
            cv2.imwrite(filename, processed)
            print(f"Foto tersimpan: {filename}")

    cap.release()
    cv2.destroyAllWindows()

if __name__ == "__main__":
    main()
