import tkinter as tk
from tkinter import filedialog, messagebox
import os
import json
import sys
import subprocess
from PIL import Image, ImageTk

# Linux için klavye kisayol modülü (keyboard veya pynput desteği)
try:
    import keyboard
except ImportError:
    try:
        from pynput import keyboard as pynput_keyboard
        keyboard = None
    except ImportError:
        keyboard = None
        pynput_keyboard = None

# Eğer program PyInstaller binary'si ise çalıştığı klasörü otomatik bul
def kaynak_yolu(relative_path):
    try:
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")
    return os.path.join(base_path, relative_path)

# Görsel ayarları
img_refs = []
BUTON_GORSEL_ADI = "fingerprint_button.png"
IKON_GORSEL_ADI = "folder_icon.png"
DELETE_GORSEL_ADI = "delete_icon.png"
SHORTCUT_GORSEL_ADI = "shortcut_icon.png"
BUTON_BOYUTU = (80, 80)
IKON_BOYUTU = (25, 25)

def load_image(path, size):
    try:
        if os.path.exists(path):
            img = Image.open(path).convert("RGBA").resize(size, Image.Resampling.LANCZOS)
            tk_img = ImageTk.PhotoImage(img)
            img_refs.append(tk_img)
            return tk_img
    except: 
        return None
    return None

AYAR_DOSYASI = "ses_ayarlari.json"

def verileri_yukle():
    if os.path.exists(AYAR_DOSYASI):
        with open(AYAR_DOSYASI, "r") as f:
            try: 
                return json.load(f)
            except: 
                pass
    return {f"f{i}": {"ses": "", "kisayol": ""} for i in range(1, 13)}

ses_yollari = verileri_yukle()
butonlar = {}
aktif_ses_prosesi = None

def verileri_kaydet():
    with open(AYAR_DOSYASI, "w") as f: 
        json.dump(ses_yollari, f, indent=4)

def herseyi_sifirla():
    global aktif_ses_prosesi
    if messagebox.askyesno("Sıfırla", "Tüm sesleri ve kısayolları silmek istiyor musunuz?"):
        if aktif_ses_prosesi:
            try:
                aktif_ses_prosesi.terminate()
            except:
                pass
            aktif_ses_prosesi = None
        if keyboard:
            try:
                keyboard.unhook_all()
            except:
                pass
        for i in range(1, 13):
            tus = f"f{i}"
            ses_yollari[tus] = {"ses": "", "kisayol": ""}
            if tus in butonlar:
                butonlar[tus].config(text=f"Boş...\n(Atanmadı)")
        verileri_kaydet()

# Linux için optimize edilmiş ses çalma fonksiyonu (PipeWire, PulseAudio veya ALSA)
def ses_cal(tus):
    global aktif_ses_prosesi
    dosya_yolu = ses_yollari[tus]["ses"]
    if dosya_yolu and os.path.exists(dosya_yolu):
        # Önceki çalan sesi durdur (üst üste binmeyi önler)
        if aktif_ses_prosesi is not None:
            try:
                aktif_ses_prosesi.terminate()
            except Exception:
                pass
            aktif_ses_prosesi = None

        for player in ["pw-play", "paplay", "aplay", "mpv", "ffplay"]:
            try:
                aktif_ses_prosesi = subprocess.Popen([player, dosya_yolu], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
                break
            except FileNotFoundError:
                continue

def kisayol_kaldir(kisayol):
    if not kisayol:
        return
    try:
        tk_key = f"<{kisayol.capitalize()}>" if (kisayol.startswith("f") and kisayol[1:].isdigit()) else kisayol
        root.unbind(tk_key)
    except:
        pass
    if keyboard:
        try:
            keyboard.remove_hotkey(kisayol)
        except:
            pass

def kisayol_ekle(kisayol, tus):
    if not kisayol:
        return
    # 1. Tkinter yerel tuş dinleyicisi (Sudo / root yetkisi gerektirmez)
    try:
        tk_key = f"<{kisayol.capitalize()}>" if (kisayol.startswith("f") and kisayol[1:].isdigit()) else kisayol
        root.bind(tk_key, lambda e, t=tus: ses_cal(t))
    except:
        pass
    # 2. Global tuş dinleyicisi (Root yetkisi varsa)
    if keyboard:
        try:
            keyboard.add_hotkey(kisayol, lambda t=tus: ses_cal(t))
        except Exception as e:
            print(f"Global kısayol eklenemedi ({kisayol}): {e}")

def dosya_sec(tus, buton_objesi):
    yeni_yol = filedialog.askopenfilename(filetypes=[("WAV Dosyaları", "*.wav"), ("Tüm Sesler", "*.wav *.mp3 *.ogg")])
    if yeni_yol:
        ses_yollari[tus]["ses"] = yeni_yol
        verileri_kaydet()
        dosya_adi = os.path.basename(yeni_yol).rsplit('.', 1)[0]
        k_yol = ses_yollari[tus]['kisayol'].upper() if ses_yollari[tus]['kisayol'] else "Atanmadı"
        buton_objesi.config(text=f"{dosya_adi[:8]}...\n({k_yol})")

def dosya_sil(tus, buton_objesi):
    if ses_yollari[tus]["kisayol"]:
        kisayol_kaldir(ses_yollari[tus]["kisayol"])
    ses_yollari[tus] = {"ses": "", "kisayol": ""}
    verileri_kaydet()
    buton_objesi.config(text=f"Boş...\n(Atanmadı)")

def kisayol_ata(tus, buton_objesi):
    dialog = tk.Toplevel(root)
    dialog.title("Kısayol Atama")
    dialog.geometry("300x150")
    dialog.focus_force()
    tk.Label(dialog, text="Lütfen bir tuşa basın...", font=("Arial", 12)).pack(pady=20)
    
    def on_key_press(event):
        yeni_key = event.keysym.lower()
        if ses_yollari[tus]["kisayol"]:
            kisayol_kaldir(ses_yollari[tus]["kisayol"])
        ses_yollari[tus]["kisayol"] = yeni_key
        kisayol_ekle(yeni_key, tus)
        verileri_kaydet()
        dosya_adi = os.path.basename(ses_yollari[tus]["ses"]).rsplit('.', 1)[0] if ses_yollari[tus]["ses"] else "Boş"
        buton_objesi.config(text=f"{dosya_adi[:8]}...\n({yeni_key.upper()})")
        dialog.destroy()
        
    dialog.bind("<Key>", on_key_press)

root = tk.Tk()
root.title("Stream Deck (Linux)")
root.geometry("530x530")
root.resizable(False, False)
root.configure(bg="#222222")

p_img_tk = load_image(kaynak_yolu(BUTON_GORSEL_ADI), BUTON_BOYUTU)
i_img_tk = load_image(kaynak_yolu(IKON_GORSEL_ADI), IKON_BOYUTU)
d_img_tk = load_image(kaynak_yolu(DELETE_GORSEL_ADI), IKON_BOYUTU)
s_img_tk = load_image(kaynak_yolu(SHORTCUT_GORSEL_ADI), IKON_BOYUTU)

for i in range(1, 13):
    tus = f"f{i}"
    data = ses_yollari[tus]
    label_text = os.path.basename(data["ses"]).rsplit('.', 1)[0] if (data["ses"] and os.path.exists(data["ses"])) else "Boş"
    k_yol = data['kisayol'].upper() if data['kisayol'] else "Atanmadı"
    
    btn = tk.Button(root, image=p_img_tk, text=f"{label_text[:8]}...\n({k_yol})", 
                    compound=tk.CENTER, fg="white", font=("Arial", 8, "bold"), bd=0, bg="#222222", activebackground="#222222",
                    command=lambda t=tus: ses_cal(t))
    btn.grid(row=(i-1)//4, column=(i-1)%4, padx=14, pady=10)
    butonlar[tus] = btn 
    
    tk.Button(root, image=d_img_tk, command=lambda t=tus, b=btn: dosya_sil(t, b), bg="#222222", bd=0, activebackground="#222222").place(in_=btn, relx=0.10, rely=0.94)
    tk.Button(root, image=s_img_tk, command=lambda t=tus, b=btn: kisayol_ata(t, b), bg="#222222", bd=0, activebackground="#222222").place(in_=btn, relx=0.35, rely=0.94)
    tk.Button(root, image=i_img_tk, command=lambda t=tus, b=btn: dosya_sec(t, b), bg="#222222", bd=0, activebackground="#222222").place(in_=btn, relx=0.60, rely=0.94)
    
    if data["kisayol"]: 
        kisayol_ekle(data["kisayol"], tus)

tk.Button(root, text="Her Şeyi Sıfırla", command=herseyi_sifirla, bg="red", fg="white", font=("Arial", 10, "bold"), activebackground="red").place(relx=0.5, rely=0.88, anchor="center")

import webbrowser

def linkedin_ac(event):
    webbrowser.open("https://www.linkedin.com/in/fthbykl/")

tasarim_label = tk.Label(root, text="Tasarım: Fatih B.", fg="gray", bg="#222222", cursor="hand2")
tasarim_label.place(relx=0.5, rely=0.96, anchor="center")
tasarim_label.bind("<Button-1>", linkedin_ac)

if __name__ == "__main__":
    root.mainloop()
