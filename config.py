# config.py
import os

# Veritabanı
DB_FILE = "japonca.db"

# Ses cache klasörü
CACHE_DIR = "audio_cache"
os.makedirs(CACHE_DIR, exist_ok=True)

# Hedef kart sayısı
HEDEF_KART = 20

# SRS aralıkları (gün)
SRS_ARALIKLAR = [1, 3, 7, 14, 30, 60, 90]

# XP seviye eşiği
LEVEL_XP = 100

# Başarı rozetleri
ROZETLER = {
    "İlk Adım": 10,
    "Çalışkan": 50,
    "Uzman": 200,
    "Japon Ustası": 500,
    "Efsane": 1000
}
