# audio.py
import os
import threading
import time
import pygame
from config import CACHE_DIR

# gTTS isteğe bağlı
try:
    from gtts import gTTS
    GTTTS_VAR = True
except ImportError:
    GTTTS_VAR = False
    print("⚠️ gTTS yüklü değil. Ses özelliği devre dışı.")

class Audio:
    def __init__(self):
        try:
            pygame.mixer.init()
            self.ses_aktif = True
        except Exception as e:
            print(f"⚠️ Ses sistemi başlatılamadı: {e}")
            self.ses_aktif = False
        self.cache_dir = CACHE_DIR

    def sesli_oku(self, metin, lang="ja"):
        if not self.ses_aktif or not GTTTS_VAR:
            return
        dosya_adi = f"{metin.replace(' ', '_').replace('/', '_')}.mp3"
        dosya_yolu = os.path.join(self.cache_dir, dosya_adi)
        if os.path.exists(dosya_yolu):
            self._play(dosya_yolu)
        else:
            try:
                tts = gTTS(text=metin, lang=lang)
                tts.save(dosya_yolu)
                self._play(dosya_yolu)
            except Exception as e:
                print(f"Ses hatası: {e}")

    def _play(self, dosya):
        def oynat():
            try:
                pygame.mixer.music.load(dosya)
                pygame.mixer.music.play()
                while pygame.mixer.music.get_busy():
                    time.sleep(0.1)
            except Exception as e:
                print(f"Çalma hatası: {e}")
        threading.Thread(target=oynat, daemon=True).start()
