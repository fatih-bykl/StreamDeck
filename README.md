# Stream Deck Uygulaması

Kendi kişisel kısayollarınızı ve seslerinizi yönetebileceğiniz, Python ve Tkinter ile geliştirilmiş pratik bir Stream Deck uygulaması.

Projede hem **Windows** hem de **Linux (CachyOS / Arch / Ubuntu)** platformları için özel olarak geliştirilmiş iki farklı sürüm bulunmaktadır.

---

## 💻 İndirme ve Sürümler

- 🪟 **Windows Versiyonu:** [`yayin_deck.py`](yayin_deck.py)
- 🐧 **Linux Versiyonu:** [`yayin_deck_linux.py`](yayin_deck_linux.py)

---

## 🚀 Özellikler
- **12 Adet Özelleştirilebilir Buton:** Her butona dilediğiniz ses dosyasını (.wav, .mp3) atayın.
- **Kısayol Atama:** İstediğiniz tuşu, atadığınız ses dosyası için bir tetikleyici olarak kullanın.
- **Çapraz Platform Ses Motoru:** Windows'ta `winsound`, Linux'ta PipeWire/PulseAudio/ALSA entegrasyonu ile kesintisiz ve akıcı ses çalma.
- **Kesintisiz Başlatma:** Aynı tuşa veya yeni bir sese basıldığında önceki ses durdurulur ve yeni ses baştan başlar.
- **Kolay Yönetim:** Ses dosyalarını seçme, kısayol atama ve temizleme işlemleri için pratik ikonlar.
- **Sıfırlama:** "Her Şeyi Sıfırla" butonu ile tüm atamaları tek seferde temizleyin.
- **Kompakt Tasarım:** Masaüstünde yer kaplamayan şık koyu tema arayüzü.

---

## 🛠 Kullanım ve Gereksinimler

### 🪟 Windows Üzerinde Çalıştırma
```bash
pip install keyboard pillow
python yayin_deck.py
```

### 🐧 Linux (CachyOS / Arch / Ubuntu) Üzerinde Çalıştırma
1. Gerekli kütüphaneleri ve Tkinter arayüz paketini kurun:
   - **Arch / CachyOS:** `sudo pacman -S tk && pip install pillow keyboard`
   - **Ubuntu / Debian:** `sudo apt install python3-tk && pip install pillow keyboard`
2. Uygulamayı çalıştırın:
   ```bash
   python3 yayin_deck_linux.py
   ```

---

## 📋 Nasıl Kullanılır?
1. Uygulamayı çalıştırın.
2. Butonların altındaki klasör ikonuna tıklayarak ses dosyanızı seçin.
3. Kısayol ikonuna tıklayarak bu ses için bir klavye tuşu atayın.
4. Artık butona tıkladığınızda veya atadığınız tuşa bastığınızda sesiniz anında çalacaktır!

---

📸 [Uygulamadan Görüntüler](uygulama_goruntusu.png)

👨‍💻 **Tasarım & Geliştirme:** Fatih B.  
🔗 [LinkedIn Profilim](https://www.linkedin.com/in/fthbykl/)

Keyifli kullanımlar!
