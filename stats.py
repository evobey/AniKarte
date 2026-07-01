# stats.py
from datetime import datetime, timedelta
from config import ROZETLER

# Matplotlib isteğe bağlı - yoksa grafik gösterimi devre dışı
try:
    import matplotlib.pyplot as plt
    MATPLOTLIB_VAR = True
except ImportError:
    MATPLOTLIB_VAR = False
    print("⚠️ matplotlib yüklü değil. Grafik özelliği devre dışı.")

class Stats:
    def __init__(self, db):
        self.db = db

    def get_rozetler(self, xp):
        kazanilan = []
        for ad, esik in ROZETLER.items():
            if xp >= esik:
                kazanilan.append(ad)
        return kazanilan

    def update_streak(self):
        user = self.db.get_user()
        if not user:
            self.db.update_user(streak=1, son_calisma=datetime.now().strftime("%Y-%m-%d"))
            return 1
        son = user[5]  # son_calisma
        bugun = datetime.now().strftime("%Y-%m-%d")
        if son is None:
            self.db.update_user(streak=1, son_calisma=bugun)
            return 1
        if son == bugun:
            return user[4]  # mevcut streak
        dün = (datetime.now() - timedelta(days=1)).strftime("%Y-%m-%d")
        if son == dün:
            yeni_streak = user[4] + 1
            self.db.update_user(streak=yeni_streak, son_calisma=bugun)
            return yeni_streak
        else:
            self.db.update_user(streak=1, son_calisma=bugun)
            return 1

    def plot_weekly(self):
        if not MATPLOTLIB_VAR:
            print("Matplotlib yüklü değil, grafik gösterilemiyor.")
            return
        hafta = self.db.get_weekly_stats()
        gunler = [g["tarih"] for g in hafta]
        dogru = [g["dogru"] for g in hafta]
        yanlis = [g["yanlis"] for g in hafta]
        plt.figure(figsize=(8, 4))
        plt.bar(gunler, dogru, label="Doğru", color="green")
        plt.bar(gunler, yanlis, bottom=dogru, label="Yanlış", color="red")
        plt.xlabel("Gün")
        plt.ylabel("Cevap Sayısı")
        plt.title("Haftalık İlerleme")
        plt.legend()
        plt.xticks(rotation=45)
        plt.tight_layout()
        plt.show()
