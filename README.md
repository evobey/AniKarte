# 🎌 AniKarte – Anime Japanese Flashcards

**AniKarte**, anime severler için özel olarak tasarlanmış, aralıklı tekrar (SRS) sistemiyle çalışan, oyunlaştırılmış bir Japonca kelime öğrenme uygulamasıdır.

## ✨ Özellikler

- 📚 **Anime Temalı Kelime Havuzu** – Naruto, One Piece, Demon Slayer ve daha fazlasından kelimeler.
- 🧠 **Aralıklı Tekrar (SRS)** – Akıllı algoritma ile unutma eğrisine göre tekrar aralıkları (1, 3, 7, 14, 30, 60, 90 gün).
- 🎮 **Oyunlaştırma** – XP puanı, level sistemi, combo, max combo, başarı rozetleri.
- 📝 **Test Modu** – 4 şıklı çoktan seçmeli test.
- ✍️ **Yazma Modu** – Romaji veya Türkçe karşılığını yazarak öğren.
- 🔊 **Sesli Okuma** – gTTS ile Japonca telaffuz (cache'li).
- 📊 **Haftalık İlerleme Grafiği** – matplotlib ile görsel analiz.
- 🖥️ **Karanlık/Aydınlık Tema** – Göz yormayan arayüz.
- 💾 **SQLite Veritabanı** – 5000+ kelime için optimize.
- 📦 **Modüler Yapı** – main, ui, data, srs, audio, stats olarak ayrılmış.
- 🌍 **Dışa/içe Aktarma** – JSON ile kelime listelerini paylaşabilirsin.

## Ekran Görüntüleri
Dark Tema <img width="1600" height="867" alt="AniKarte_DarkMod" src="https://github.com/user-attachments/assets/c1cfbe06-6f78-48d9-b915-c7f0f0c036e9" />
White Tema <img width="1600" height="867" alt="AniKarte_WhiteMod" src="https://github.com/user-attachments/assets/4adc5c5f-3a72-47db-bc71-7dcdba452ba9" />

## 🖼️ Kısayollar

| Tuş | İşlev |
|-----|-------|
| `Enter` | Anlamı göster / sesli oku |
| `Sağ Ok` | Bildim (doğru) |
| `Sol Ok` | Bilemedim (yanlış) |
| `R` | Romaji aç/kapa |
| `T` | Test modu aç/kapa |
| `Y` | Yazma modu aç/kapa |
| `D` | Karanlık/aydınlık tema değiştir |

## 🚀 Kurulum

```bash
# 1. Depoyu klonla
git clone https://github.com/evobey/AniKarte.git
cd AniKarte

# 2. Sanal ortam oluştur (önerilen)
python3 -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate

# 3. Bağımlılıkları yükle
pip install -r requirements.txt

# 4. Çalıştır
python main.py

📦 Bağımlılıklar

    Python 3.8+

    tkinter (genelde yüklü gelir)

    gtts (ses için)

    pygame (ses oynatmak için)

    matplotlib (grafikler için, isteğe bağlı)

bash

# Tüm bağımlılıklar
pip install gtts pygame matplotlib

🧩 Katkıda Bulunma

Projeye katkıda bulunmak çok kolay!

    Bu depoyu fork'la.

    Kendi branch'ini oluştur (git checkout -b ozellik/harika-ekleme).

    Değişikliklerini commit et (git commit -m 'Harika bir özellik ekledim').

    Branch'ini pushla (git push origin ozellik/harika-ekleme).

    Bir Pull Request oluştur.

📄 Lisans

Bu proje MIT lisansı ile lisanslanmıştır – detaylar için LICENSE dosyasına bakın.
🙏 Teşekkürler

    Anime topluluğuna ilham için

    Tüm açık kaynak kütüphanelerin geliştiricilerine

✨ İyi çalışmalar ve 頑張って (Ganbatte)! 🎌
