import pygame
import random
import os

# Oyun ekranı boyutları
GENISLIK = 400
YUKSEKLIK = 600

pygame.init()
ekran = pygame.display.set_mode((GENISLIK, YUKSEKLIK))
pygame.display.set_caption("Flappy Bird")

# Renkler
BEYAZ = (255, 255, 255)
SIYAH = (0, 0, 0)
MAVI = (0, 155, 255)
YESIL = (0, 200, 0)

# Kuş resmini yükle
try:
    kus_resmi = pygame.image.load("kus.png")  # "kus.png" yerine fotoğrafın dosya adını yaz
    kus_resmi = pygame.transform.scale(kus_resmi, (30, 30))  # Boyutunu ayarla
except:
    print("Kuş resmi yüklenemedi, varsayılan daire kullanılacak")
    kus_resmi = None

# Kuş özellikleri
kus_x = 50
kus_y = 300
kus_y_hizi = 0
yercekimi = 0.5

# Boru özellikleri
boru_genislik = 70
boru_bosluk = 150
borular = []

def yeni_boru():
    yukseklik = random.randint(100, 400)
    borular.append({"x": GENISLIK, "y": yukseklik})

saat = pygame.time.Clock()
puan = 0
font = pygame.font.SysFont(None, 36)

# İlk boru
yeni_boru()

oyun_bitti = False
while True:
    ekran.fill(MAVI)

    for etkinlik in pygame.event.get():
        if etkinlik.type == pygame.QUIT:
            pygame.quit()
            quit()
        if etkinlik.type == pygame.KEYDOWN and not oyun_bitti:
            if etkinlik.key == pygame.K_SPACE:
                kus_y_hizi = -8

    if not oyun_bitti:
        kus_y_hizi += yercekimi
        kus_y += kus_y_hizi

        # Yeni boru ekle
        if borular[-1]["x"] < 200:
            yeni_boru()

        # Boruları güncelle
        yeni_borular = []
        for boru in borular:
            boru["x"] -= 3
            if boru["x"] + boru_genislik > 0:
                yeni_borular.append(boru)
            if boru["x"] == kus_x:
                puan += 1
        borular = yeni_borular

        # Kuşu ve boruları çiz
        if kus_resmi:
            # Resmi döndürme (kuşun hareketine göre)
            rotated_kus = pygame.transform.rotate(kus_resmi, -kus_y_hizi * 2)
            ekran.blit(rotated_kus, (kus_x - 15, kus_y - 15))
        else:
            pygame.draw.circle(ekran, SIYAH, (kus_x, int(kus_y)), 15)
            
        for boru in borular:
            pygame.draw.rect(ekran, YESIL, (boru["x"], 0, boru_genislik, boru["y"]))
            pygame.draw.rect(ekran, YESIL, (boru["x"], boru["y"] + boru_bosluk, boru_genislik, YUKSEKLIK))

        # Çarpışma kontrolü
        for boru in borular:
            if (kus_x + 15 > boru["x"] and kus_x - 15 < boru["x"] + boru_genislik):
                if kus_y < boru["y"] or kus_y > boru["y"] + boru_bosluk:
                    oyun_bitti = True

        if kus_y > YUKSEKLIK or kus_y < 0:
            oyun_bitti = True

    else:
        bitis_mesaji = font.render("Oyun Bitti! R = Yeniden", True, SIYAH)
        ekran.blit(bitis_mesaji, (100, 250))
        tuslar = pygame.key.get_pressed()
        if tuslar[pygame.K_r]:
            kus_y = 300
            kus_y_hizi = 0
            borular = []
            yeni_boru()
            puan = 0
            oyun_bitti = False

    # Puan gösterimi
    puan_yazi = font.render(f"Puan: {puan}", True, BEYAZ)
    ekran.blit(puan_yazi, (10, 10))

    pygame.display.update()
    saat.tick(60)