# ui.py
import tkinter as tk
from tkinter import ttk, messagebox
from config import HEDEF_KART

class UI:
    def __init__(self, root, app):
        self.root = root
        self.app = app
        self.create_widgets()

    def create_widgets(self):
        # Üst panel
        self.ust_frame = tk.Frame(self.root, bg="#eee", padx=10, pady=5)
        self.ust_frame.pack(fill="x", side="top")

        self.lbl_hedef = tk.Label(self.ust_frame, text=f"🔥 Hedef: 0 / {HEDEF_KART}",
                                  font=("Segoe UI", 10, "bold"), bg="#eee")
        self.lbl_hedef.pack(side="left")

        # Filtreler
        filter_frame = tk.Frame(self.ust_frame, bg="#eee")
        filter_frame.pack(side="left", padx=10)

        tk.Label(filter_frame, text="JLPT:", bg="#eee", font=("Segoe UI", 9)).pack(side="left")
        self.jlpt_var = tk.StringVar(value="Tümü")
        jlpt_menu = ttk.Combobox(filter_frame, textvariable=self.jlpt_var,
                                 values=["Tümü", "N5", "N4", "N3", "N2", "N1"], width=6)
        jlpt_menu.pack(side="left", padx=3)
        jlpt_menu.bind("<<ComboboxSelected>>", lambda e: self.app.filtrele())

        tk.Label(filter_frame, text="Tür:", bg="#eee", font=("Segoe UI", 9)).pack(side="left")
        self.tur_var = tk.StringVar(value="Tümü")
        tur_menu = ttk.Combobox(filter_frame, textvariable=self.tur_var,
                                values=["Tümü", "Hiragana", "Katakana", "Kanji", "Karışık"], width=8)
        tur_menu.pack(side="left", padx=3)
        tur_menu.bind("<<ComboboxSelected>>", lambda e: self.app.filtrele())

        tk.Label(filter_frame, text="Anime:", bg="#eee", font=("Segoe UI", 9)).pack(side="left")
        self.anime_var = tk.StringVar(value="Tümü")
        anime_menu = ttk.Combobox(filter_frame, textvariable=self.anime_var,
                                  values=["Tümü", "Naruto", "One Piece", "Demon Slayer", "Dragon Ball", "Bleach", "Attack on Titan", "Fairy Tail", "Genel"], width=10)
        anime_menu.pack(side="left", padx=3)
        anime_menu.bind("<<ComboboxSelected>>", lambda e: self.app.filtrele())

        # Sağdaki kontroller
        sag_frame = tk.Frame(self.ust_frame, bg="#eee")
        sag_frame.pack(side="right")

        # Ses
        self.ses_var = tk.BooleanVar(value=True)
        chk_ses = tk.Checkbutton(sag_frame, text="🔊 Ses", variable=self.ses_var,
                                 bg="#eee", font=("Segoe UI", 9))
        chk_ses.pack(side="left", padx=5)

        # Romaji
        self.romaji_var = tk.BooleanVar(value=False)
        chk_romaji = tk.Checkbutton(sag_frame, text="Romaji (R)", variable=self.romaji_var,
                                    bg="#eee", font=("Segoe UI", 9))
        chk_romaji.pack(side="left", padx=5)

        # Tema
        btn_tema = tk.Button(sag_frame, text="🌓 Tema (D)", command=self.app.tema_toggle,
                             font=("Segoe UI", 9), bg="#ddd")
        btn_tema.pack(side="left", padx=5)

        # Mod göstergeleri
        self.lbl_test_durum = tk.Label(sag_frame, text="Test: KAPALI (T)", bg="#eee",
                                       font=("Segoe UI", 9, "bold"), fg="#555")
        self.lbl_test_durum.pack(side="left", padx=5)

        self.lbl_yazma_durum = tk.Label(sag_frame, text="Yazma: KAPALI (Y)", bg="#eee",
                                        font=("Segoe UI", 9, "bold"), fg="#555")
        self.lbl_yazma_durum.pack(side="left", padx=5)

        # Kart alanı
        self.kart_frame = tk.Frame(self.root, bg="white", highlightbackground="#ddd", highlightthickness=1)
        self.kart_frame.pack(fill="both", expand=True, padx=20, pady=20)

        self.japonca_etiket = tk.Label(self.kart_frame, text="", font=("Yu Gothic UI", 32, "bold"),
                                       bg="white", fg="#111")
        self.japonca_etiket.pack(pady=(20, 5))

        self.romaji_etiket = tk.Label(self.kart_frame, text="", font=("Segoe UI", 12, "italic"),
                                      bg="white", fg="#666")
        self.romaji_etiket.pack(pady=2)

        self.kanji_etiket = tk.Label(self.kart_frame, text="", font=("Segoe UI", 11),
                                     bg="white", fg="#2d7d2d")
        self.kanji_etiket.pack(pady=2)

        self.turkce_etiket = tk.Label(self.kart_frame, text="", font=("Segoe UI", 16),
                                      bg="white", fg="#d9534f")
        self.turkce_etiket.pack(pady=15)

        # Bildirim etiketi (mesaj kutusu yerine)
        self.bildirim_etiket = tk.Label(self.kart_frame, text="", font=("Segoe UI", 12, "bold"),
                                        bg="white", fg="#5cb85c")
        self.bildirim_etiket.pack(pady=5)

        # Yazma modu
        self.yazma_frame = tk.Frame(self.kart_frame, bg="white")
        self.yazma_frame.pack_forget()
        self.yazma_entry = tk.Entry(self.yazma_frame, font=("Segoe UI", 14), width=25)
        self.yazma_entry.pack(side="left", padx=5)
        self.btn_yazma_kontrol = tk.Button(self.yazma_frame, text="Kontrol Et",
                                           font=("Segoe UI", 10, "bold"), bg="#5bc0de", fg="white")
        self.btn_yazma_kontrol.pack(side="left", padx=5)

        # Test butonları
        self.test_butonlari = []
        test_frame = tk.Frame(self.kart_frame, bg="white")
        test_frame.pack(pady=5)
        for i in range(4):
            btn = tk.Button(test_frame, text="", font=("Segoe UI", 12),
                           state="disabled", width=25)
            btn.pack(pady=2)
            self.test_butonlari.append(btn)

        # Butonlar
        self.buton_frame = tk.Frame(self.root, bg="#fafafa")
        self.buton_frame.pack(pady=5)

        self.btn_goster = tk.Button(self.buton_frame, text="Anlamını Göster (Enter)",
                                    font=("Segoe UI", 11, "bold"), bg="#0275d8",
                                    fg="white", padx=15, pady=5)
        self.btn_goster.pack(pady=3)

        self.degerlendirme_frame = tk.Frame(self.buton_frame, bg="#fafafa")
        self.degerlendirme_frame.pack(pady=3)

        self.btn_bildim = tk.Button(self.degerlendirme_frame, text="✔ Bildim (Sağ ok)",
                                    font=("Segoe UI", 10, "bold"), bg="#5cb85c",
                                    fg="white", state="disabled", padx=10)
        self.btn_bildim.pack(side="left", padx=5)

        self.btn_bilemedim = tk.Button(self.degerlendirme_frame, text="❌ Bilemedim (Sol ok)",
                                       font=("Segoe UI", 10, "bold"), bg="#d9534f",
                                       fg="white", state="disabled", padx=10)
        self.btn_bilemedim.pack(side="left", padx=5)

        # Progress
        self.progress_frame = tk.Frame(self.root, bg="#fafafa")
        self.progress_frame.pack(fill="x", padx=20, pady=5)
        self.progress_bar = ttk.Progressbar(self.progress_frame, orient="horizontal",
                                            length=600, mode="determinate")
        self.progress_bar.pack()

        # Puan ve grafik
        puan_frame = tk.Frame(self.root, bg="#fafafa")
        puan_frame.pack(fill="x", padx=20, pady=5)
        self.lbl_puan = tk.Label(puan_frame, text="⭐ XP: 0  |  Level: 1  |  Combo: 0  |  Max Combo: 0",
                                 font=("Segoe UI", 10, "bold"), bg="#fafafa", fg="#333")
        self.lbl_puan.pack(side="left")
        self.lbl_grafik = tk.Label(puan_frame, text="📊 Bu hafta: henüz veri yok",
                                   font=("Segoe UI", 10), bg="#fafafa", fg="#555")
        self.lbl_grafik.pack(side="right")

        # Alt panel
        self.alt_frame = tk.Frame(self.root, bg="#f1f1f1", pady=5)
        self.alt_frame.pack(fill="x", side="bottom")

        self.lbl_stats = tk.Label(self.alt_frame, text="Doğru: 0  |  Yanlış: 0  |  Başarı: %0  |  Zorlar: Yok",
                                  font=("Segoe UI", 9), bg="#f1f1f1", fg="#555")
        self.lbl_stats.pack()

        info = tk.Label(self.alt_frame, text="💡 Kısayollar: Enter (göster) | Sağ/Sol ok | R (romaji) | T (test) | Y (yazma) | D (tema)",
                        font=("Segoe UI", 8), bg="#f1f1f1", fg="#999")
        info.pack()

        # Buton komutlarını bağla (app metodları)
        self.btn_goster.config(command=self.app.cevabi_goster)
        self.btn_bildim.config(command=lambda: self.app.cevap_ver(True))
        self.btn_bilemedim.config(command=lambda: self.app.cevap_ver(False))
        self.btn_yazma_kontrol.config(command=self.app.yazma_kontrol)
        # Test butonlarına komut ata
        for i, btn in enumerate(self.test_butonlari):
            btn.config(command=lambda idx=i: self.app.test_cevap(idx))