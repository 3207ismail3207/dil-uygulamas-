import pygame
import random

# Pygame'i başlat
pygame.init()

# Ekran boyutları ve renkler
SCREEN_WIDTH, SCREEN_HEIGHT = 800, 600

# Modern renk paleti
WHITE = (255, 255, 255)
BLACK = (40, 44, 52)
BLUE = (88, 101, 242)    # Discord Blue
RED = (255, 88, 88)      # Soft Red
GREEN = (87, 242, 135)    # Neon Green
YELLOW = (255, 205, 86)   # Soft Yellow
LIGHT_GRAY = (241, 243, 244)
DARK_GRAY = (54, 57, 63)  # Discord Dark
PRIMARY = (114, 137, 218) # Modern Purple
SECONDARY = (66, 184, 131) # Mint Green
ACCENT = (255, 170, 102)   # Soft Orange
BG_COLOR = (47, 49, 54)    # Discord Background

# Yazı tipleri ve boyutları
try:
    FONT_LARGE = pygame.font.SysFont('Arial', 48)
    FONT_MEDIUM = pygame.font.SysFont('Arial', 32)
    FONT_SMALL = pygame.font.SysFont('Arial', 24)
    FONT_BUTTON = pygame.font.SysFont('Arial', 28)
except:
    FONT_LARGE = pygame.font.Font(None, 60)
    FONT_MEDIUM = pygame.font.Font(None, 40)
    FONT_SMALL = pygame.font.Font(None, 30)
    FONT_BUTTON = pygame.font.Font(None, 36)

# Avatar dosya yolları
AVATAR_LIST = ["avatar1.jpg", "avatar2.jpg", "avatar3.jpg", "avatar4.jpg"]

# Kelime listeleri - zorluk seviyelerine göre
easy_words = {
    "apple": "elma",
    "book": "kitap",
    "cat": "kedi",
    "dog": "köpek",
    "school": "okul",
    "house": "ev",
    "water": "su",
    "food": "yiyecek",
    "play": "oynamak",
    "run": "koşmak",
    "jump": "zıplamak",
    "read": "okumak",
    "write": "yazmak",
    "game": "oyun",
    "color": "renk",
    "size": "boyut",
    "shape": "şekil",
    "happy": "mutlu",
    "sad": "üzgün",
    "help": "yardım"
}

medium_words = {
    "friend": "arkadaş",
    "family": "aile",
    "teacher": "öğretmen",
    "student": "öğrenci",
    "class": "sınıf",
    "homework": "ödev",
    "music": "müzik",
    "art": "sanat",
    "science": "bilim",
    "math": "matematik",
    "history": "tarih",
    "sports": "sporlar",
    "movie": "film",
    "phone": "telefon",
    "city": "şehir",
    "country": "ülke",
    "nature": "doğa",
    "animal": "hayvan",
    "plant": "bitki",
    "weather": "hava durumu"
}

hard_words = {
    "television": "televizyon",
    "computer": "bilgisayar",
    "internet": "internet",
    "travel": "seyahat",
    "vacation": "tatil",
    "season": "mevsim",
    "holiday": "tatil",
    "party": "parti",
    "gift": "hediye",
    "dream": "rüya",
    "story": "hikaye",
    "adventure": "macera",
    "friendship": "arkadaşlık",
    "happiness": "mutluluk",
    "sadness": "üzüntü",
    "kindness": "nazik olmak",
    "bravery": "cesaret",
    "honesty": "dürüstlük",
    "respect": "saygı",
    "love": "aşk"
}

# Aktif kelime listesi ve puan sistemi
active_words = easy_words.copy()
current_level = "easy"  # Varsayılan seviye

# Zorluk seviyelerine göre puan sistemi
level_points = {
    "easy": 5,    # Kolay seviye - doğru cevap başına 5 puan
    "medium": 10, # Orta seviye - doğru cevap başına 10 puan
    "hard": 15    # Zor seviye - doğru cevap başına 15 puan
}

# Görsel yolları
BACKGROUND_IMAGE = "arkaplan.jpg"  # Arka plan görseli
GREEN_TICK = "yeşiltık.jpg"
RED_CROSS = "kırmızıçarpı.jpg"

# Ekran oluştur
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Dil Öğrenme Oyunu")

# Kullanıcı bilgileri
user_data = {
    "name": "",
    "score": 0,
    "avatar": AVATAR_LIST[0],  # Varsayılan avatar
}

# Çizim fonksiyonları
def draw_text(surface, text, font, color, x, y):
    text_obj = font.render(text, True, color)
    text_rect = text_obj.get_rect(center=(x, y))
    surface.blit(text_obj, text_rect)

def draw_button(surface, text, font, color, rect_color, x, y, w, h, hover=False):
    # Buton gölgesi
    shadow_color = tuple(max(0, c - 20) for c in rect_color)
    pygame.draw.rect(surface, shadow_color, (x+2, y+2, w, h), border_radius=15)
    
    # Ana buton
    if hover:
        # Hover efekti için rengi biraz aydınlat ve parlaklık efekti ekle
        hover_color = tuple(min(255, c + 40) for c in rect_color)
        glow_surface = pygame.Surface((w+10, h+10), pygame.SRCALPHA)
        pygame.draw.rect(glow_surface, (*hover_color, 100), (0, 0, w+10, h+10), border_radius=15)
        surface.blit(glow_surface, (x-5, y-5))
        pygame.draw.rect(surface, hover_color, (x, y, w, h), border_radius=15)
    else:
        pygame.draw.rect(surface, rect_color, (x, y, w, h), border_radius=15)
    
    # Buton kenarı - daha ince ve şık
    border_color = tuple(min(255, c + 30) for c in rect_color)
    pygame.draw.rect(surface, border_color, (x, y, w, h), border_radius=15, width=1)
    
    # Metin gölgesi - daha yumuşak
    draw_text(surface, text, font, (*BLACK, 100), x + w // 2 + 1, y + h // 2 + 1)
    # Metin
    draw_text(surface, text, font, color, x + w // 2, y + h // 2)

def draw_image(surface, image_path, x, y):
    """Görseli belirtilen koordinatlarda çizer."""
    try:
        image = pygame.image.load(image_path)
        image = pygame.transform.scale(image, (100, 100))  # Görseli yeniden boyutlandır
        surface.blit(image, (x, y))
    except pygame.error:
        print(f"Görsel yüklenirken hata oluştu: {image_path}")

def draw_background():
    """Arka plan görselini çizer."""
    try:
        background = pygame.image.load(BACKGROUND_IMAGE)
        background = pygame.transform.scale(background, (SCREEN_WIDTH, SCREEN_HEIGHT))
        screen.blit(background, (0, 0))
    except pygame.error:
        print(f"Arkaplan görseli yüklenirken hata oluştu: {BACKGROUND_IMAGE}")

# Avatar seçim ekranı
def avatar_selection_screen():
    running = True
    selected_avatar = user_data["avatar"]

    while running:
        draw_background()
        draw_text(screen, "Avatar Seçimi", FONT_LARGE, BLACK, SCREEN_WIDTH // 2, 150)

        # Avatarları göster
        for i, avatar in enumerate(AVATAR_LIST):
            x = 150 + (i * 150)
            y = 250
            draw_image(screen, avatar, x, y)
            # Seçilen avatarı işaretle
            if selected_avatar == avatar:
                pygame.draw.rect(screen, BLUE, (x - 10, y - 10, 120, 120), 3)  # Seçilen avatarın etrafına çerçeve

        pygame.display.flip()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
                pygame.quit()
                return None
            if event.type == pygame.MOUSEBUTTONDOWN:
                for i, avatar in enumerate(AVATAR_LIST):
                    x = 150 + (i * 150)
                    y = 250
                    if x <= event.pos[0] <= x + 100 and y <= event.pos[1] <= y + 100:
                        selected_avatar = avatar
                        user_data["avatar"] = selected_avatar
                        pygame.time.wait(500)
                        return "main_menu"

def welcome_screen():
    running = True
    user_name = ""
    input_active = False
    cursor_visible = True
    cursor_timer = 0

    while running:
        draw_background()
        
        # Başlık alanı
        pygame.draw.rect(screen, PRIMARY, (0, 60, SCREEN_WIDTH, 100))
        draw_text(screen, "Dil Öğrenme Oyunu", FONT_LARGE, WHITE, SCREEN_WIDTH // 2, 110)
        
        # Alt başlık
        draw_text(screen, "Adınızı yazın ve Enter'a basın", FONT_MEDIUM, BLACK, SCREEN_WIDTH // 2, 220)

        # Modern metin kutusu
        input_box = pygame.Rect(SCREEN_WIDTH//2 - 150, 280, 300, 50)
        # Metin kutusu gölgesi
        pygame.draw.rect(screen, DARK_GRAY, (input_box.x+2, input_box.y+2, input_box.width, input_box.height), border_radius=10)
        # Metin kutusu arka planı
        pygame.draw.rect(screen, WHITE, input_box, border_radius=10)
        # Metin kutusu kenarı
        pygame.draw.rect(screen, PRIMARY if input_active else LIGHT_GRAY, input_box, border_radius=10, width=2)
        
        # Girilen metni göster (SADECE BURADA ÇİZİYORUZ)
        cursor_timer = (cursor_timer + 1) % 60
        cursor_visible = cursor_timer < 30
        display_text = user_name + ("_" if cursor_visible and input_active else "")
        
        # Eğer metin kutusu boşsa placeholder göster
        if len(display_text) == 0 or (len(display_text) == 1 and display_text == "_"):
            draw_text(screen, "Adınızı yazın...", FONT_MEDIUM, (*DARK_GRAY, 150), SCREEN_WIDTH // 2, 305)
        else:
            draw_text(screen, display_text, FONT_MEDIUM, BLACK, SCREEN_WIDTH // 2, 305)

        pygame.display.flip()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
                pygame.quit()
                return False

            if event.type == pygame.MOUSEBUTTONDOWN:
                if input_box.collidepoint(event.pos):
                    input_active = True
                else:
                    input_active = False

            if event.type == pygame.KEYDOWN and input_active:
                if event.key == pygame.K_RETURN:
                    user_data["name"] = user_name if user_name.strip() != "" else "Oyuncu"
                    return True
                elif event.key == pygame.K_BACKSPACE:
                    user_name = user_name[:-1]
                else:
                    user_name += event.unicode

def main_menu():
    global active_words  # Aktif kelime listesini global olarak kullan
    
    # Ana menü butonları
    main_buttons = [
        {"text": "Kolay Seviye", "action": "easy", "color": GREEN},
        {"text": "Orta Seviye", "action": "medium", "color": YELLOW},
        {"text": "Zor Seviye", "action": "hard", "color": RED},
        {"text": "Puan Durumu", "action": "score", "color": SECONDARY},
        {"text": "Avatar Seç", "action": "avatar_selection", "color": ACCENT},
        {"text": "Çıkış", "action": "exit", "color": (*DARK_GRAY, 200)}
    ]

    running = True
    button_height = 60
    button_spacing = 20
    total_height = len(main_buttons) * (button_height + button_spacing) - button_spacing
    start_y = (SCREEN_HEIGHT - total_height) // 2

    while running:
        screen.fill(BG_COLOR)
        
        # Başlık alanı - gradient efekti
        for i in range(80):
            progress = i / 80
            color = tuple(int(a + (b-a)*progress) for a, b in zip(PRIMARY, (*PRIMARY[:2], min(255, PRIMARY[2]+50))))
            pygame.draw.rect(screen, color, (0, i, SCREEN_WIDTH, 1))
        
        # Başlık parlaklık efekti
        glow = pygame.Surface((SCREEN_WIDTH, 80), pygame.SRCALPHA)
        for i in range(20):
            alpha = int(255 * (1 - i/20))
            pygame.draw.rect(glow, (*WHITE, alpha), (0, 80-i, SCREEN_WIDTH, 1))
        screen.blit(glow, (0, 0))
        
        draw_text(screen, f"Hoş Geldin, {user_data['name']}!", FONT_LARGE, WHITE, SCREEN_WIDTH // 2, 40)
        
        # Avatar gösterimi - modern stil
        avatar_size = 100
        avatar_x = 50
        avatar_y = 100
        # Avatar arka plan efekti
        glow_avatar = pygame.Surface((avatar_size+20, avatar_size+20), pygame.SRCALPHA)
        pygame.draw.circle(glow_avatar, (*PRIMARY, 50), (avatar_size//2+10, avatar_size//2+10), avatar_size//2 + 10)
        screen.blit(glow_avatar, (avatar_x-10, avatar_y-10))
        pygame.draw.circle(screen, WHITE, (avatar_x + avatar_size//2, avatar_y + avatar_size//2), avatar_size//2 + 2)
        draw_image(screen, user_data["avatar"], avatar_x, avatar_y)
        
        # Skor gösterimi - modern stil
        score_box = pygame.Rect(avatar_x - 10, avatar_y + avatar_size + 20, avatar_size + 20, 40)
        pygame.draw.rect(screen, (*PRIMARY, 30), score_box, border_radius=10)
        draw_text(screen, f"Puan: {user_data['score']}", FONT_MEDIUM, PRIMARY, score_box.centerx, score_box.centery)

        mouse_pos = pygame.mouse.get_pos()
        
        # Butonları çiz - modern stil
        for i, button in enumerate(main_buttons):
            button_rect = pygame.Rect(SCREEN_WIDTH//2 - 150, start_y + i*(button_height + button_spacing), 300, button_height)
            hover = button_rect.collidepoint(mouse_pos)
            # Modern buton çizimi
            draw_button(screen, button["text"], FONT_BUTTON, WHITE, button["color"], button_rect.x, button_rect.y, button_rect.width, button_rect.height, hover)
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return None
            elif event.type == pygame.MOUSEBUTTONDOWN:
                # Tıklanan butonu kontrol et
                for button in main_buttons:
                    button_rect = pygame.Rect(SCREEN_WIDTH//2 - 150, start_y + main_buttons.index(button)*(button_height + button_spacing), 300, button_height)
                    if button_rect.collidepoint(event.pos):
                        if button["action"] in ["easy", "medium", "hard"]:
                            # Zorluk seviyesine göre kelime listesini ve seviyeyi güncelle
                            global current_level
                            if button["action"] == "easy":
                                active_words = easy_words.copy()
                                current_level = "easy"
                            elif button["action"] == "medium":
                                active_words = medium_words.copy()
                                current_level = "medium"
                            else:
                                active_words = hard_words.copy()
                                current_level = "hard"
                            return "translate"
                        return button["action"]

        pygame.display.flip()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
                pygame.quit()
                return None
            if event.type == pygame.MOUSEBUTTONDOWN:
                if 250 <= event.pos[0] <= 550 and 200 <= event.pos[1] <= 250:
                    return "translate"
                elif 250 <= event.pos[0] <= 550 and 300 <= event.pos[1] <= 350:
                    return "score"
                elif 250 <= event.pos[0] <= 550 and 400 <= event.pos[1] <= 450:
                    return "avatar_selection"
                elif 250 <= event.pos[0] <= 550 and 500 <= event.pos[1] <= 550:
                    return "exit"
def translate_game():
    running = True
    word = random.choice(list(active_words.keys()))
    correct_answer = active_words[word]
    user_input = ""
    attempts_left = 3
    feedback = None
    feedback_timer = 0
    cursor_visible = True
    cursor_timer = 0

    while running:
        screen.fill(BG_COLOR)  # Modern arka plan rengi
        
        # Başlık alanı - gradient efekti
        for i in range(80):
            progress = i / 80
            color = tuple(int(a + (b-a)*progress) for a, b in zip(PRIMARY, (*PRIMARY[:2], min(255, PRIMARY[2]+50))))
            pygame.draw.rect(screen, color, (0, i, SCREEN_WIDTH, 1))
        pygame.draw.rect(screen, (*DARK_GRAY, 150), (0, 80, SCREEN_WIDTH, 2))
        draw_text(screen, "Kelime Çevirisi", FONT_LARGE, WHITE, SCREEN_WIDTH // 2, 40)
        
        # Kelime kartı - modern görünüm
        card_rect = pygame.Rect(SCREEN_WIDTH//2 - 200, 120, 400, 120)
        # Kart gölgesi ve parlaklık efekti
        glow_surface = pygame.Surface((card_rect.width+20, card_rect.height+20), pygame.SRCALPHA)
        pygame.draw.rect(glow_surface, (*PRIMARY, 30), (0, 0, card_rect.width+20, card_rect.height+20), border_radius=20)
        screen.blit(glow_surface, (card_rect.x-10, card_rect.y-10))
        # Kart arka planı - gradient
        for i in range(card_rect.height):
            progress = i / card_rect.height
            color = tuple(int(a + (b-a)*progress) for a, b in zip(WHITE, (245, 245, 250)))
            pygame.draw.rect(screen, color, (card_rect.x, card_rect.y+i, card_rect.width, 1), border_radius=20)
        # Kart kenarı - ince ve şık
        pygame.draw.rect(screen, (*PRIMARY, 150), card_rect, border_radius=20, width=1)
        # Kelimeyi ve seviye bilgisini göster
        level_text = {
            "easy": "Kolay Seviye (5 puan)",
            "medium": "Orta Seviye (10 puan)",
            "hard": "Zor Seviye (15 puan)"
        }[current_level]
        
        draw_text(screen, level_text, FONT_SMALL, PRIMARY, SCREEN_WIDTH // 2, 130)
        draw_text(screen, f"İngilizce kelime:", FONT_SMALL, DARK_GRAY, SCREEN_WIDTH // 2, 160)
        draw_text(screen, word, FONT_LARGE, PRIMARY, SCREEN_WIDTH // 2, 190)
        
        # Modern cevap kutusu
        input_box = pygame.Rect(SCREEN_WIDTH//2 - 150, 280, 300, 50)
        
        # Giriş kutusu efektleri
        glow_input = pygame.Surface((input_box.width+20, input_box.height+20), pygame.SRCALPHA)
        pygame.draw.rect(glow_input, (*PRIMARY, 30), (0, 0, input_box.width+20, input_box.height+20), border_radius=15)
        screen.blit(glow_input, (input_box.x-10, input_box.y-10))
        
        # Ana kutu
        pygame.draw.rect(screen, (*WHITE, 255), input_box, border_radius=15)
        pygame.draw.rect(screen, (*PRIMARY, 150), input_box, border_radius=15, width=2)
        
        # Cevabı göster - modern stil
        cursor_timer = (cursor_timer + 1) % 60
        cursor_visible = cursor_timer < 30

        if len(display_text) > 0:
         draw_text(screen, display_text, FONT_MEDIUM, PRIMARY, SCREEN_WIDTH // 2, 305)
        else:
            # Placeholder text
            draw_text(screen, "Türkçe karşılığını yazın...", FONT_MEDIUM, DARK_GRAY, SCREEN_WIDTH // 2, 305)

        # Kalan hakları göster
        for i in range(attempts_left):
            heart_x = SCREEN_WIDTH//2 - 50 + i*50
            pygame.draw.circle(screen, RED, (heart_x, 380), 15)
            pygame.draw.circle(screen, RED, (heart_x+15, 380), 15)
            pygame.draw.polygon(screen, RED, [(heart_x-15, 380), (heart_x+30, 380), (heart_x+7.5, 410)])
        
        # Geri bildirim görselini çiz
        if feedback:
            if feedback == "correct":
                draw_image(screen, GREEN_TICK, SCREEN_WIDTH // 2 - 25, 450)
            elif feedback == "wrong":
                draw_image(screen, RED_CROSS, SCREEN_WIDTH // 2 - 25, 450)
            
            # Geri bildirim süresi kontrolü
            feedback_timer += 1
            if feedback_timer >= 60:  # 1 saniye bekle
                if feedback == "correct":
                    # Yeni kelimeye geç
                    word = random.choice(list(active_words.keys()))
                    correct_answer = active_words[word]
                    user_input = ""
                    feedback = None
                    feedback_timer = 0
                else:
                    feedback = None
                    feedback_timer = 0

        # Geri bildirim görselini çizin
        if feedback == "correct":
            draw_image(screen, GREEN_TICK, SCREEN_WIDTH // 2 - 50, 400)
        elif feedback == "fail":
            draw_image(screen, RED_CROSS, SCREEN_WIDTH // 2 - 50, 400)

        pygame.display.flip()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
                pygame.quit()
                return None
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:
                    if user_input.lower() == correct_answer.lower():
                        user_data["score"] += 10
                        feedback = "correct"
                        # Yeşil tık göster
                        draw_image(screen, GREEN_TICK, SCREEN_WIDTH // 2 - 50, 400)
                        pygame.display.flip()
                        pygame.time.wait(1000)  # Yeşil tık gösterim süresi
                        # Yeni kelimeye geç
                        word = random.choice(list(active_words.keys()))
                        correct_answer = active_words[word]
                        user_input = ""
                        feedback = None
                        # Puan durumu kontrolü
                        if user_data["score"] >= 50:  # 50 puanla yeni bölüme geç
                            return "new_level"
                    else:
                        attempts_left -= 1
                        feedback = "fail"
                        if attempts_left == 0:
                            draw_text(screen, f"Yanlış! Doğru cevap: {correct_answer}", FONT_LARGE, RED, SCREEN_WIDTH // 2, 450)
                            pygame.display.flip()
                            pygame.time.wait(3000)
                            return "fail"
                elif event.key == pygame.K_BACKSPACE:
                    user_input = user_input[:-1]
                else:
                    user_input += event.unicode

# Yeni bir seviye ekleyelim
def new_level():
    running = True
    while running:
        draw_background()
        draw_text(screen, "Yeni Bölüm: Orta Zorluk", FONT_LARGE, BLUE, SCREEN_WIDTH // 2, 150)
        draw_text(screen, "Başlamak için herhangi bir tuşa basın", FONT_MEDIUM, BLACK, SCREEN_WIDTH // 2, 250)
        pygame.display.flip()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
                pygame.quit()
                return None
            if event.type == pygame.KEYDOWN:
                return "translate"  # Yeni zorlukla kelime çevirisi başlatılacak

# Zaman sınırlı oyun
def time_limit_game():
    start_ticks = pygame.time.get_ticks()  # Zamanı başlat
    time_limit = 30  # 30 saniye
    running = True
    word = random.choice(list(active_words.keys()))
    correct_answer = active_words[word]
    user_input = ""
    attempts_left = 3
    feedback = None  # Geri bildirim görselini saklamak için

    while running:
        draw_background()
        draw_text(screen, f"İngilizce kelime: {word}", FONT_MEDIUM, BLACK, SCREEN_WIDTH // 2, 150)
        draw_text(screen, f"Cevabınız: {user_input}", FONT_MEDIUM, BLUE, SCREEN_WIDTH // 2, 250)
        draw_text(screen, f"Kalan Hak: {attempts_left}", FONT_MEDIUM, RED, SCREEN_WIDTH // 2, 350)
        
        # Kalan süreyi göster
        seconds = (pygame.time.get_ticks() - start_ticks) // 1000
        remaining_time = max(0, time_limit - seconds)
        draw_text(screen, f"Süre: {remaining_time}s", FONT_MEDIUM, RED, SCREEN_WIDTH // 2, 450)

        # Zaman bittiğinde oyun bitir
        if remaining_time == 0:
            draw_text(screen, "Zaman doldu!", FONT_LARGE, RED, SCREEN_WIDTH // 2, 500)
            pygame.display.flip()
            pygame.time.wait(2000)
            return "fail"

        # Geri bildirim görselini çizin
        if feedback == "correct":
            draw_image(screen, GREEN_TICK, SCREEN_WIDTH // 2 - 50, 400)
        elif feedback == "fail":
            draw_image(screen, RED_CROSS, SCREEN_WIDTH // 2 - 50, 400)

        pygame.display.flip()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
                pygame.quit()
                return None
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN and not feedback:
                    if user_input.lower() == correct_answer.lower():
                        user_data["score"] += 10
                        feedback = "correct"
                        feedback_timer = 0
                    else:
                        attempts_left -= 1
                        feedback = "wrong"
                        feedback_timer = 0
                        if attempts_left == 0:
                            draw_text(screen, f"Yanlış! Doğru cevap: {correct_answer}", FONT_LARGE, RED, SCREEN_WIDTH // 2, 450)
                            pygame.display.flip()
                            pygame.time.wait(1000)
                            return "fail"
                elif event.key == pygame.K_BACKSPACE and not feedback:
                    user_input = user_input[:-1]
                elif not feedback:
                    user_input += event.unicode

# Puan çeşitlendirmesi
def bonus_points_game():
    running = True
    word = random.choice(list(active_words.keys()))
    correct_answer = active_words[word]
    user_input = ""
    attempts_left = 3
    feedback = None  # Geri bildirim görselini saklamak için

    while running:
        draw_background()
        draw_text(screen, f"İngilizce kelime: {word}", FONT_MEDIUM, BLACK, SCREEN_WIDTH // 2, 150)
        draw_text(screen, f"Cevabınız: {user_input}", FONT_MEDIUM, BLUE, SCREEN_WIDTH // 2, 250)
        draw_text(screen, f"Kalan Hak: {attempts_left}", FONT_MEDIUM, RED, SCREEN_WIDTH // 2, 350)

        # Bonus Puan
        if user_input.lower() == correct_answer.lower():
            user_data["score"] += 5  # Ekstra bonus puan

        # Geri bildirim görselini çizin
        if feedback == "correct":
            draw_image(screen, GREEN_TICK, SCREEN_WIDTH // 2 - 50, 400)
        elif feedback == "fail":
            draw_image(screen, RED_CROSS, SCREEN_WIDTH // 2 - 50, 400)

        pygame.display.flip()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
                pygame.quit()
                return None
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:
                    if user_input.lower() == correct_answer.lower():
                        # Zorluk seviyesine göre puan ekle
                        user_data["score"] += level_points[current_level]
                        feedback = "correct"
                        pygame.display.flip()
                        pygame.time.wait(2000)
                        return "correct"
                    else:
                        attempts_left -= 1
                        feedback = "fail"
                        if attempts_left == 0:
                            draw_text(screen, f"Yanlış! Doğru cevap: {correct_answer}", FONT_LARGE, RED, SCREEN_WIDTH // 2, 450)
                            pygame.display.flip()
                            pygame.time.wait(3000)
                            return "fail"
                elif event.key == pygame.K_BACKSPACE:
                    user_input = user_input[:-1]
                else:
                    user_input += event.unicode

def show_score():
    running = True
    while running:
        draw_background()
        
        # Başlık alanı
        pygame.draw.rect(screen, PRIMARY, (0, 0, SCREEN_WIDTH, 80))
        pygame.draw.rect(screen, DARK_GRAY, (0, 80, SCREEN_WIDTH, 4))
        draw_text(screen, "Puan Durumu", FONT_LARGE, WHITE, SCREEN_WIDTH // 2, 40)
        
        # Puan kartı
        card_rect = pygame.Rect(SCREEN_WIDTH//2 - 200, 120, 400, 200)
        # Kart gölgesi
        pygame.draw.rect(screen, DARK_GRAY, (card_rect.x+4, card_rect.y+4, card_rect.width, card_rect.height), border_radius=15)
        # Kart arka planı
        pygame.draw.rect(screen, WHITE, card_rect, border_radius=15)
        # Kart kenarı
        pygame.draw.rect(screen, PRIMARY, card_rect, border_radius=15, width=2)
        
        # Kullanıcı bilgileri
        avatar_size = 80
        avatar_x = SCREEN_WIDTH//2 - avatar_size//2
        avatar_y = 140
        pygame.draw.circle(screen, WHITE, (avatar_x + avatar_size//2, avatar_y + avatar_size//2), avatar_size//2 + 5)
        draw_image(screen, user_data["avatar"], avatar_x, avatar_y)
        
        # Kullanıcı adı ve puanı
        draw_text(screen, user_data['name'], FONT_MEDIUM, PRIMARY, SCREEN_WIDTH // 2, 250)
        draw_text(screen, f"Toplam Puan: {user_data['score']}", FONT_LARGE, SECONDARY, SCREEN_WIDTH // 2, 290)
        
        # Geri dönüş mesajı
        pygame.draw.rect(screen, LIGHT_GRAY, (SCREEN_WIDTH//2 - 250, 380, 500, 60), border_radius=10)
        draw_text(screen, "Ana menüye dönmek için herhangi bir tuşa basın", FONT_SMALL, DARK_GRAY, SCREEN_WIDTH // 2, 410)
        pygame.display.flip()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
                return
            if event.type == pygame.KEYDOWN:
                return

# Ana döngü
if welcome_screen():
    while True:
        choice = main_menu()
        if choice == "translate":
            level_result = translate_game()
            if level_result == "new_level":
                new_level()  # Yeni bölüme geç
        elif choice == "score":
            show_score()
        elif choice == "avatar_selection":
            avatar_selection_screen()
        elif choice == "exit":
            print("Oyundan çıkılıyor...")
            pygame.quit()
            break
        
        # Eğer choice None ise (pencere kapatıldıysa)
        if choice is None:
            pygame.quit()
            break