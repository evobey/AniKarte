# srs.py
from datetime import datetime, timedelta
from config import SRS_ARALIKLAR

class SRS:
    @staticmethod
    def filtrele(kelimeler, aktif=True):
        if not aktif:
            return kelimeler
        simdi = datetime.now()
        sonuc = []
        for k in kelimeler:
            # k: (id, japonca, romaji, turkce, jlpt, tur, anime, onyomi, kunyomi, dogru, yanlis, tekrar_araligi, son_tekrar, sira)
            son_tekrar = k[12]
            if son_tekrar is None:
                sonuc.append(k)
            else:
                aralik = k[11] if k[11] else 1
                son = datetime.fromisoformat(son_tekrar)
                if (simdi - son).days >= aralik:
                    sonuc.append(k)
        return sonuc if sonuc else kelimeler

    @staticmethod
    def guncelle(kelime, bilindi):
        # kelime: tuple
        mevcut_aralik = kelime[11] if kelime[11] else 1
        if bilindi:
            if mevcut_aralik in SRS_ARALIKLAR:
                idx = SRS_ARALIKLAR.index(mevcut_aralik)
                if idx < len(SRS_ARALIKLAR) - 1:
                    yeni = SRS_ARALIKLAR[idx + 1]
                else:
                    yeni = SRS_ARALIKLAR[-1]
            else:
                yeni = SRS_ARALIKLAR[0]
        else:
            yeni = SRS_ARALIKLAR[0]
        son_tekrar = datetime.now().isoformat()
        return yeni, son_tekrar