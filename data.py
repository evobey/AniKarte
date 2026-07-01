# data.py
import sqlite3
import json
from datetime import datetime, timedelta  # <--- EKLENDİ
from config import DB_FILE
from datetime import datetime, timedelta

class Database:
    def __init__(self):
        self.conn = sqlite3.connect(DB_FILE)
        self.cursor = self.conn.cursor()
        self._create_tables()
        self._init_default_data()

    def _create_tables(self):
        # Kelimeler tablosu
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS kelimeler (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                japonca TEXT NOT NULL,
                romaji TEXT,
                turkce TEXT NOT NULL,
                jlpt TEXT,
                tur TEXT,
                anime TEXT,
                onyomi TEXT,
                kunyomi TEXT,
                dogru INTEGER DEFAULT 0,
                yanlis INTEGER DEFAULT 0,
                tekrar_araligi INTEGER DEFAULT 1,
                son_tekrar TEXT,
                sira INTEGER DEFAULT 0
            )
        ''')
        # İlerleme tablosu (günlük)
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS ilerleme (
                tarih TEXT PRIMARY KEY,
                dogru INTEGER DEFAULT 0,
                yanlis INTEGER DEFAULT 0,
                xp INTEGER DEFAULT 0
            )
        ''')
        # Kullanıcı tablosu (XP, level, max_combo, streak)
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS kullanici (
                id INTEGER PRIMARY KEY,
                xp INTEGER DEFAULT 0,
                level INTEGER DEFAULT 1,
                max_combo INTEGER DEFAULT 0,
                streak INTEGER DEFAULT 0,
                son_calisma TEXT
            )
        ''')
        self.conn.commit()

    def _init_default_data(self):
        # Varsayılan kelimeler (eğer tablo boşsa)
        self.cursor.execute("SELECT COUNT(*) FROM kelimeler")
        if self.cursor.fetchone()[0] == 0:
            default = [
                ("こんにちは", "Konnichiwa", "Merhaba", "N5", "Hiragana", "Genel", "", ""),
                ("学生", "Gakusei", "Öğrenci", "N5", "Kanji", "Genel", "ガク", "まなぶ"),
                ("ありがとう", "Arigatou", "Teşekkür ederim", "N5", "Hiragana", "Genel", "", ""),
                ("カメラ", "Kamera", "Kamera", "N5", "Katakana", "Genel", "", ""),
                ("美味しい", "Oishii", "Lezzetli", "N5", "Karışık", "Genel", "", ""),
                ("忍", "Shinobi", "Ninja", "N4", "Kanji", "Naruto", "ニン", "しのぶ"),
                ("海賊", "Kaizoku", "Korsan", "N4", "Kanji", "One Piece", "カイゾク", ""),
                ("鬼", "Oni", "İblis", "N4", "Kanji", "Demon Slayer", "キ", "おに"),
                ("魂", "Tamashii", "Ruh", "N3", "Kanji", "Bleach", "コン", "たましい"),
                ("悪魔", "Akuma", "Şeytan", "N4", "Kanji", "Black Clover", "アクマ", ""),
            ]
            for kelime in default:
                self.cursor.execute('''
                    INSERT INTO kelimeler 
                    (japonca, romaji, turkce, jlpt, tur, anime, onyomi, kunyomi)
                    VALUES (?, ?, ?, ?, ?, ?, ?, ?)
                ''', kelime)
            self.conn.commit()

        # Varsayılan kullanıcı
        self.cursor.execute("SELECT COUNT(*) FROM kullanici")
        if self.cursor.fetchone()[0] == 0:
            self.cursor.execute("INSERT INTO kullanici (id, xp, level) VALUES (1, 0, 1)")
            self.conn.commit()

    # ----- Kelime işlemleri -----
    def get_all_words(self):
        self.cursor.execute("SELECT * FROM kelimeler")
        return self.cursor.fetchall()

    def get_words_by_filter(self, jlpt=None, tur=None, anime=None):
        query = "SELECT * FROM kelimeler WHERE 1=1"
        params = []
        if jlpt and jlpt != "Tümü":
            query += " AND jlpt = ?"
            params.append(jlpt)
        if tur and tur != "Tümü":
            query += " AND tur = ?"
            params.append(tur)
        if anime and anime != "Tümü":
            query += " AND anime = ?"
            params.append(anime)
        self.cursor.execute(query, params)
        return self.cursor.fetchall()

    def get_word_by_id(self, id):
        self.cursor.execute("SELECT * FROM kelimeler WHERE id = ?", (id,))
        return self.cursor.fetchone()

    def update_word_stats(self, id, dogru_artis, yanlis_artis, tekrar_araligi, son_tekrar):
        self.cursor.execute('''
            UPDATE kelimeler 
            SET dogru = dogru + ?, yanlis = yanlis + ?, 
                tekrar_araligi = ?, son_tekrar = ?
            WHERE id = ?
        ''', (dogru_artis, yanlis_artis, tekrar_araligi, son_tekrar, id))
        self.conn.commit()

    # ----- İlerleme -----
    def get_today_progress(self, tarih=None):
        if not tarih:
            tarih = datetime.now().strftime("%Y-%m-%d")
        self.cursor.execute("SELECT dogru, yanlis, xp FROM ilerleme WHERE tarih = ?", (tarih,))
        row = self.cursor.fetchone()
        if row:
            return {"dogru": row[0], "yanlis": row[1], "xp": row[2]}
        return {"dogru": 0, "yanlis": 0, "xp": 0}

    def update_today_progress(self, dogru_artis=0, yanlis_artis=0, xp_artis=0):
        tarih = datetime.now().strftime("%Y-%m-%d")
        self.cursor.execute('''
            INSERT INTO ilerleme (tarih, dogru, yanlis, xp)
            VALUES (?, ?, ?, ?)
            ON CONFLICT(tarih) DO UPDATE SET
                dogru = dogru + ?,
                yanlis = yanlis + ?,
                xp = xp + ?
        ''', (tarih, dogru_artis, yanlis_artis, xp_artis, dogru_artis, yanlis_artis, xp_artis))
        self.conn.commit()

    def get_weekly_stats(self):
        """Son 7 günün verilerini döndür"""
        bugun = datetime.now()
        hafta = []
        for i in range(7):
            gun = (bugun - timedelta(days=i)).strftime("%Y-%m-%d")
            self.cursor.execute("SELECT dogru, yanlis, xp FROM ilerleme WHERE tarih = ?", (gun,))
            row = self.cursor.fetchone()
            if row:
                hafta.append({"tarih": gun, "dogru": row[0], "yanlis": row[1], "xp": row[2]})
            else:
                hafta.append({"tarih": gun, "dogru": 0, "yanlis": 0, "xp": 0})
        return hafta

    # ----- Kullanıcı -----
    def get_user(self):
        self.cursor.execute("SELECT * FROM kullanici WHERE id = 1")
        return self.cursor.fetchone()

    def update_user(self, xp=None, level=None, max_combo=None, streak=None, son_calisma=None):
        updates = []
        params = []
        if xp is not None:
            updates.append("xp = ?")
            params.append(xp)
        if level is not None:
            updates.append("level = ?")
            params.append(level)
        if max_combo is not None:
            updates.append("max_combo = ?")
            params.append(max_combo)
        if streak is not None:
            updates.append("streak = ?")
            params.append(streak)
        if son_calisma is not None:
            updates.append("son_calisma = ?")
            params.append(son_calisma)
        if updates:
            query = "UPDATE kullanici SET " + ", ".join(updates) + " WHERE id = 1"
            self.cursor.execute(query, params)
            self.conn.commit()

    # ----- Dışa/içe aktarma -----
    def export_to_json(self, filename="kelimeler_export.json"):
        self.cursor.execute("SELECT * FROM kelimeler")
        rows = self.cursor.fetchall()
        columns = [desc[0] for desc in self.cursor.description]
        data = [dict(zip(columns, row)) for row in rows]
        with open(filename, "w", encoding="utf-8") as f:
            json.dump(data, f, ensure_ascii=False, indent=2)

    def import_from_json(self, filename):
        with open(filename, "r", encoding="utf-8") as f:
            data = json.load(f)
        for item in data:
            self.cursor.execute('''
                INSERT INTO kelimeler 
                (japonca, romaji, turkce, jlpt, tur, anime, onyomi, kunyomi, dogru, yanlis, tekrar_araligi, son_tekrar, sira)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            ''', (
                item.get("japonca"), item.get("romaji"), item.get("turkce"),
                item.get("jlpt"), item.get("tur"), item.get("anime"),
                item.get("onyomi"), item.get("kunyomi"), 0, 0, 1, None, 0
            ))
        self.conn.commit()
