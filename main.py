# main.py
import tkinter as tk
import random
from datetime import datetime, timedelta
from data import Database
from srs import SRS
from audio import Audio
from stats import Stats
from ui import UI
from config import HEDEF_KART

class FlashcardApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Japonca Kartları v6.0 - Profesyonel")
        self.root.geometry("850x750")
        self.root.configure(bg="#fafafa")

        # Veritabanı
        self.db = Database()

        # Ses
        self.audio = Audio()

        # SRS
        self.srs = SRS()

        # İstatistikler
        self.stats = Stats(self.db)

        # Arayüz
        self.ui = UI(root, self)

        # Değişkenler
        self.mevcut_kelime = None
        self.toplam_calisilan = 0
        self.karanlik_mod = False
        self.test_modu = False
        self.yazma_modu = False
        self.srs_aktif = True
        self.combo = 0
        self.max_combo = 0
        self.xp = 0
        self.level = 1

        # Kullanıcı verisini yükle
        self.kullanici_yukle()

        # Filtrele ve ilk kartı göster
        self.filtrele()
        self.yeni_kelime_getir()
        self.istatistikleri_guncelle()
        self.puan_guncelle()
        self.grafik_guncelle()

        # Klavye kısayolları
        self.root.bind("<Return>", lambda e: self.cevabi_goster())
        self.root.bind("<Right>", lambda e: self.cevap_ver(True))
        self.root.bind("<Left>", lambda e: self.cevap_ver(False))
        self.root.bind("<r>", lambda e: self.romaji_toggle())
        self.root.bind("<R>", lambda e: self.romaji_toggle())
        self.root.bind("<t>", lambda e: self.test_toggle())
        self.root.bind("<T>", lambda e: self.test_toggle())
        self.root.bind("<y>", lambda e: self.yazma_toggle())
        self.root.bind("<Y>", lambda e: self.yazma_toggle())
        self.root.bind("<d>", lambda e: self.tema_toggle())
        self.root.bind("<D>", lambda e: self.tema_toggle())

    # ----- Kullanıcı verisi -----
    def kullanici_yukle(self):
        user = self.db.get_user()
        if user:
            self.xp = user[1]
            self.level = user[2]
            self.max_combo = user[3]
            # streak kontrolü
            self.stats.update_streak()

    # ----- Filtreleme -----
    def filtrele(self):
        jlpt = self.ui.jlpt_var.get()
        tur = self.ui.tur_var.get()
        anime = self.ui.anime_var.get()
        self.kelimeler = self.db.get_words_by_filter(jlpt, tur, anime)
        # SRS uygula
        self.kelimeler = SRS.filtrele(self.kelimeler, self.srs_aktif)
        if not self.kelimeler:
            self.kelimeler = self.db.get_words_by_filter(jlpt, tur, anime)
        self.yeni_kelime_getir()

    # ----- Ağırlıklı seçim -----
    def agirlikli_sec(self, liste):
        if not liste:
            return None
        agirliklar = [max(1, k[10] + 1) for k in liste]  # yanlis + 1
        for i, k in enumerate(liste):
            if k[9] > 5:  # dogru
                agirliklar[i] = max(1, agirliklar[i] - k[9] // 2)
        return random.choices(liste, weights=agirliklar, k=1)[0]

    # ----- Yeni kelime -----
    def yeni_kelime_getir(self):
        if not self.kelimeler:
            self.filtrele()
        if self.kelimeler:
            self.mevcut_kelime = self.agirlikli_sec(self.kelimeler) or random.choice(self.kelimeler)
            # UI'ı güncelle
            self.ui.japonca_etiket.config(text=self.mevcut_kelime[1])  # japonca
            self.ui.turkce_etiket.config(text="")
            self.ui.romaji_etiket.config(text="")
            onyomi = self.mevcut_kelime[7] if self.mevcut_kelime[7] else ""
            kunyomi = self.mevcut_kelime[8] if self.mevcut_kelime[8] else ""
            kanji_bilgi = ""
            if onyomi:
                kanji_bilgi += f"音読み: {onyomi}  "
            if kunyomi:
                kanji_bilgi += f"訓読み: {kunyomi}"
            self.ui.kanji_etiket.config(text=kanji_bilgi)
            self.ui.btn_goster.config(state="normal")
            self.ui.btn_bildim.config(state="disabled")
            self.ui.btn_bilemedim.config(state="disabled")
            self.ui.bildirim_etiket.config(text="")
            # Test/yazma modları
            if self.test_modu:
                self.test_goster()
            elif self.yazma_modu:
                self.ui.yazma_entry.delete(0, tk.END)
                self.ui.yazma_entry.focus()
                self.ui.yazma_frame.pack(pady=5)
                self.ui.btn_yazma_kontrol.config(state="normal")
            else:
                self.ui.yazma_frame.pack_forget()
                self.test_butonlarini_gizle()
            self.progress_guncelle()

    # ----- Test modu -----
    def test_goster(self):
        self.ui.turkce_etiket.config(text="Hangi anlam?")
        self.ui.romaji_etiket.config(text="")
        self.ui.kanji_etiket.config(text="")
        self.ui.btn_goster.config(state="disabled")
        self.ui.btn_bildim.config(state="disabled")
        self.ui.btn_bilemedim.config(state="disabled")
        self.ui.yazma_frame.pack_forget()
        # 4 seçenek oluştur
        dogru = self.mevcut_kelime[3]  # turkce
        digerleri = [k[3] for k in self.db.get_all_words() if k[3] != dogru]
        secenekler = [dogru] + random.sample(digerleri, min(3, len(digerleri)))
        while len(secenekler) < 4:
            secenekler.append("???")
        random.shuffle(secenekler)
        for i, btn in enumerate(self.ui.test_butonlari):
            btn.config(text=secenekler[i], state="normal", bg="#f0f0f0")
            btn.pack()

    def test_butonlarini_gizle(self):
        for btn in self.ui.test_butonlari:
            btn.pack_forget()

    def test_cevap(self, index):
        secilen = self.ui.test_butonlari[index].cget("text")
        dogru = self.mevcut_kelime[3]
        if secilen == dogru:
            self.cevap_sonuc(True)
            self.ui.bildirim_etiket.config(text=f"✅ Doğru! +{self.combo*2+10} XP", fg="green")
        else:
            self.cevap_sonuc(False)
            self.ui.bildirim_etiket.config(text=f"❌ Yanlış! Doğru: {dogru}", fg="red")
        self.test_butonlarini_gizle()
        self.root.after(1500, lambda: self.ui.bildirim_etiket.config(text=""))
        self.yeni_kelime_getir()

    def test_toggle(self):
        self.test_modu = not self.test_modu
        durum = "AÇIK" if self.test_modu else "KAPALI"
        self.ui.lbl_test_durum.config(text=f"Test: {durum} (T)")
        if self.test_modu:
            self.yazma_modu = False
            self.ui.lbl_yazma_durum.config(text="Yazma: KAPALI (Y)")
            self.ui.yazma_frame.pack_forget()
        self.yeni_kelime_getir()

    # ----- Yazma modu -----
    def yazma_toggle(self):
        self.yazma_modu = not self.yazma_modu
        durum = "AÇIK" if self.yazma_modu else "KAPALI"
        self.ui.lbl_yazma_durum.config(text=f"Yazma: {durum} (Y)")
        if self.yazma_modu:
            self.test_modu = False
            self.ui.lbl_test_durum.config(text="Test: KAPALI (T)")
            self.ui.yazma_entry.delete(0, tk.END)
            self.ui.yazma_entry.focus()
        self.yeni_kelime_getir()

    def yazma_kontrol(self):
        if not self.mevcut_kelime:
            return
        cevap = self.ui.yazma_entry.get().strip().lower()
        dogru_romaji = self.mevcut_kelime[2].lower()
        dogru_turkce = self.mevcut_kelime[3].lower()
        if cevap == dogru_romaji or cevap == dogru_turkce:
            self.cevap_sonuc(True)
            self.ui.bildirim_etiket.config(text=f"✅ Doğru! +{self.combo*2+10} XP", fg="green")
        else:
            self.cevap_sonuc(False)
            self.ui.bildirim_etiket.config(text=f"❌ Yanlış! Doğru: {dogru_romaji} / {dogru_turkce}", fg="red")
        self.root.after(1500, lambda: self.ui.bildirim_etiket.config(text=""))
        self.yeni_kelime_getir()

    # ----- Cevap mekanizması -----
    def cevabi_goster(self):
        if not self.mevcut_kelime or self.test_modu or self.yazma_modu:
            return
        self.ui.turkce_etiket.config(text=self.mevcut_kelime[3])  # turkce
        if self.ui.romaji_var.get():
            self.ui.romaji_etiket.config(text=f"[{self.mevcut_kelime[2]}]")
        else:
            self.ui.romaji_etiket.config(text="")
        self.ui.btn_goster.config(state="disabled")
        self.ui.btn_bildim.config(state="normal")
        self.ui.btn_bilemedim.config(state="normal")
        if self.ui.ses_var.get():
            self.audio.sesli_oku(self.mevcut_kelime[1])

    def cevap_ver(self, bilindi_mi):
        if self.test_modu or self.yazma_modu:
            return
        if not self.mevcut_kelime:
            return
        if self.ui.btn_bildim["state"] == "disabled":
            return
        self.cevap_sonuc(bilindi_mi)
        self.yeni_kelime_getir()

    def cevap_sonuc(self, bilindi_mi):
        if not self.mevcut_kelime:
            return
        self.toplam_calisilan += 1
        kelime_id = self.mevcut_kelime[0]
        dogru_artis = 1 if bilindi_mi else 0
        yanlis_artis = 0 if bilindi_mi else 1
        # SRS güncelle
        yeni_aralik, son_tekrar = SRS.guncelle(self.mevcut_kelime, bilindi_mi)
        self.db.update_word_stats(kelime_id, dogru_artis, yanlis_artis, yeni_aralik, son_tekrar)

        # XP ve combo
        if bilindi_mi:
            self.combo += 1
            if self.combo > self.max_combo:
                self.max_combo = self.combo
            xp_kazan = 10 + self.combo * 2
            self.xp += xp_kazan
            # Level kontrol
            yeni_level = self.xp // 100 + 1
            if yeni_level > self.level:
                self.level = yeni_level
                self.ui.bildirim_etiket.config(text=f"🎊 Level Atladın! Level {self.level}", fg="gold")
                self.root.after(3000, lambda: self.ui.bildirim_etiket.config(text=""))
        else:
            self.combo = 0

        # Günlük ilerleme
        self.db.update_today_progress(dogru_artis, yanlis_artis, xp_kazan if bilindi_mi else 0)

        # Kullanıcı güncelle
        self.db.update_user(xp=self.xp, level=self.level, max_combo=self.max_combo)

        # Streak güncelle
        self.stats.update_streak()

        # UI güncelle
        self.istatistikleri_guncelle()
        self.puan_guncelle()
        self.grafik_guncelle()
        self.progress_guncelle()

    def romaji_toggle(self):
        self.ui.romaji_var.set(not self.ui.romaji_var.get())
        if self.mevcut_kelime and self.ui.turkce_etiket.cget("text") != "":
            self.cevabi_goster()

    # ----- Tema -----
    def tema_toggle(self):
        self.karanlik_mod = not self.karanlik_mod
        if self.karanlik_mod:
            renkler = {"bg": "#1e1e1e", "fg": "#ffffff", "kart": "#2d2d2d"}
        else:
            renkler = {"bg": "#fafafa", "fg": "#111111", "kart": "#ffffff"}
        self.root.configure(bg=renkler["bg"])
        self.ui.ust_frame.configure(bg=renkler["bg"])
        self.ui.kart_frame.configure(bg=renkler["kart"], highlightbackground="#555")
        self.ui.japonca_etiket.configure(bg=renkler["kart"], fg=renkler["fg"])
        self.ui.romaji_etiket.configure(bg=renkler["kart"], fg="#aaa")
        self.ui.turkce_etiket.configure(bg=renkler["kart"], fg="#ff6b6b")
        self.ui.kanji_etiket.configure(bg=renkler["kart"], fg="#6bff6b")
        self.ui.alt_frame.configure(bg=renkler["bg"])
        self.ui.lbl_stats.configure(bg=renkler["bg"], fg=renkler["fg"])
        self.ui.lbl_hedef.configure(bg=renkler["bg"], fg=renkler["fg"])
        self.ui.lbl_test_durum.configure(bg=renkler["bg"], fg=renkler["fg"])
        self.ui.lbl_yazma_durum.configure(bg=renkler["bg"], fg=renkler["fg"])
        self.ui.lbl_puan.configure(bg=renkler["bg"], fg=renkler["fg"])
        self.ui.lbl_grafik.configure(bg=renkler["bg"], fg=renkler["fg"])
        self.ui.bildirim_etiket.configure(bg=renkler["kart"])

    # ----- Bilgi panelleri -----
    def istatistikleri_guncelle(self):
        toplam_dogru = sum(k[9] for k in self.db.get_all_words())
        toplam_yanlis = sum(k[10] for k in self.db.get_all_words())
        toplam_cevap = toplam_dogru + toplam_yanlis
        basari = (toplam_dogru / toplam_cevap * 100) if toplam_cevap > 0 else 0
        zorlar = sorted(self.db.get_all_words(), key=lambda x: x[10], reverse=True)[:3]
        zor_metin = " | ".join([f"{k[1]} ({k[10]})" for k in zorlar if k[10] > 0]) or "Yok"
        self.ui.lbl_stats.config(text=f"Doğru: {toplam_dogru}  |  Yanlış: {toplam_yanlis}  |  Başarı: %{basari:.0f}  |  Zorlar: {zor_metin}")

    def progress_guncelle(self):
        deger = min(100, (self.toplam_calisilan / HEDEF_KART) * 100)
        self.ui.progress_bar["value"] = deger
        metin = f"🔥 Hedef: {self.toplam_calisilan} / {HEDEF_KART}"
        if self.toplam_calisilan >= HEDEF_KART:
            metin += " 🎉 Tamamlandı!"
        self.ui.lbl_hedef.config(text=metin)

    def puan_guncelle(self):
        rozetler = self.stats.get_rozetler(self.xp)
        rozet_str = " | ".join(rozetler) if rozetler else "Henüz yok"
        self.ui.lbl_puan.config(text=f"⭐ XP: {self.xp}  |  Level: {self.level}  |  Combo: {self.combo}  |  Max Combo: {self.max_combo}  |  Rozetler: {rozet_str}")

    def grafik_guncelle(self):
        hafta = self.db.get_weekly_stats()
        toplam = sum(g["dogru"] + g["yanlis"] for g in hafta)
        dogru_top = sum(g["dogru"] for g in hafta)
        if toplam == 0:
            self.ui.lbl_grafik.config(text="📊 Bu hafta henüz çalışma yok.")
            return
        oran = (dogru_top / toplam) * 100
        bar = "█" * int(oran // 5) + "░" * (20 - int(oran // 5))
        self.ui.lbl_grafik.config(text=f"📊 Bu hafta: {bar} %{oran:.0f}  (Doğru: {dogru_top} / {toplam})")

if __name__ == "__main__":
    root = tk.Tk()
    app = FlashcardApp(root)
    root.mainloop()