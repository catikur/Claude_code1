#!/usr/bin/env python3
"""
Zar Atma Oyunu
- Kaç yüzlü zar kullanılacağını seçin
- Kaç oyuncu oynayacağını belirleyin
- Sırayla zarları atın!
"""

import random
import time
import os

def clear_screen():
    """Ekranı temizle"""
    os.system('cls' if os.name == 'nt' else 'clear')

def print_banner():
    """Oyun başlığını göster"""
    print("""
    ╔═══════════════════════════════════════╗
    ║         🎲  ZAR ATMA OYUNU  🎲        ║
    ╚═══════════════════════════════════════╝
    """)

def get_dice_art(value, max_value):
    """Zar değeri için ASCII art oluştur"""
    if max_value == 6:
        # 6 yüzlü zar için özel görsel
        dice_faces = {
            1: [
                "┌─────────┐",
                "│         │",
                "│    ●    │",
                "│         │",
                "└─────────┘"
            ],
            2: [
                "┌─────────┐",
                "│ ●       │",
                "│         │",
                "│       ● │",
                "└─────────┘"
            ],
            3: [
                "┌─────────┐",
                "│ ●       │",
                "│    ●    │",
                "│       ● │",
                "└─────────┘"
            ],
            4: [
                "┌─────────┐",
                "│ ●     ● │",
                "│         │",
                "│ ●     ● │",
                "└─────────┘"
            ],
            5: [
                "┌─────────┐",
                "│ ●     ● │",
                "│    ●    │",
                "│ ●     ● │",
                "└─────────┘"
            ],
            6: [
                "┌─────────┐",
                "│ ●     ● │",
                "│ ●     ● │",
                "│ ●     ● │",
                "└─────────┘"
            ]
        }
        return dice_faces[value]
    else:
        # Diğer zarlar için genel görsel
        value_str = str(value)
        padding = (7 - len(value_str)) // 2
        return [
            "┌─────────┐",
            "│         │",
            f"│{' ' * padding}{value_str}{' ' * (7 - padding - len(value_str))}│",
            "│         │",
            "└─────────┘"
        ]

def rolling_animation(max_value):
    """Zar atma animasyonu"""
    frames = ["🎲", "🎯", "✨", "💫"]
    print("\n    Zar atılıyor", end="", flush=True)
    for _ in range(3):
        for frame in frames:
            print(f"\r    Zar atılıyor {frame}", end="", flush=True)
            time.sleep(0.1)
    print("\r" + " " * 30 + "\r", end="")

def display_result(player_name, value, max_value):
    """Sonucu güzel bir şekilde göster"""
    dice_art = get_dice_art(value, max_value)

    print(f"\n    {player_name} zarı attı!")
    print()
    for line in dice_art:
        print(f"        {line}")
    print(f"\n    🎯 Sonuç: {value}")
    print("    " + "─" * 25)

def get_positive_integer(prompt, min_val=1, max_val=1000):
    """Kullanıcıdan pozitif tam sayı al"""
    while True:
        try:
            value = int(input(prompt))
            if min_val <= value <= max_val:
                return value
            else:
                print(f"    ⚠️  Lütfen {min_val} ile {max_val} arasında bir sayı girin.")
        except ValueError:
            print("    ⚠️  Lütfen geçerli bir sayı girin.")

def play_round(players, dice_sides):
    """Bir tur oyna"""
    results = {}

    for i, player in enumerate(players, 1):
        input(f"\n    👉 {player}, zarı atmak için ENTER'a bas...")
        rolling_animation(dice_sides)
        result = random.randint(1, dice_sides)
        display_result(player, result, dice_sides)
        results[player] = result

    return results

def show_round_summary(results, round_num):
    """Tur özeti göster"""
    print(f"\n    ╔═══════════════════════════════════╗")
    print(f"    ║      📊 {round_num}. TUR ÖZETİ             ║")
    print(f"    ╠═══════════════════════════════════╣")

    max_score = max(results.values())
    winners = [player for player, score in results.items() if score == max_score]

    for player, score in results.items():
        marker = " 🏆" if score == max_score else "   "
        print(f"    ║  {player:15} : {score:3}{marker}       ║")

    print(f"    ╚═══════════════════════════════════╝")

    if len(winners) == 1:
        print(f"\n    🎉 Bu turun kazananı: {winners[0]}!")
    else:
        print(f"\n    🤝 Berabere! Kazananlar: {', '.join(winners)}")

def main():
    """Ana oyun döngüsü"""
    clear_screen()
    print_banner()

    # Oyun ayarları
    print("    📋 OYUN AYARLARI")
    print("    " + "─" * 25)

    dice_sides = get_positive_integer("\n    🎲 Kaç yüzlü zar? (örn: 6, 12, 20): ", 2, 100)
    num_players = get_positive_integer("    👥 Kaç oyuncu var? (1-10): ", 1, 10)

    # Oyuncu isimleri
    players = []
    print(f"\n    📝 Oyuncu isimlerini girin:")
    for i in range(1, num_players + 1):
        name = input(f"    Oyuncu {i} ismi: ").strip()
        if not name:
            name = f"Oyuncu {i}"
        players.append(name)

    # Toplam skorlar
    total_scores = {player: 0 for player in players}
    round_num = 0

    # Oyun döngüsü
    while True:
        round_num += 1
        clear_screen()
        print_banner()
        print(f"    🎮 {dice_sides} yüzlü zar ile oynuyorsunuz")
        print(f"    📍 Tur: {round_num}")
        print("    " + "═" * 35)

        # Turu oyna
        results = play_round(players, dice_sides)

        # Skorları güncelle
        for player, score in results.items():
            total_scores[player] += score

        # Tur özeti
        show_round_summary(results, round_num)

        # Toplam skorları göster
        if round_num > 1:
            print(f"\n    📈 TOPLAM SKORLAR:")
            for player, score in sorted(total_scores.items(), key=lambda x: -x[1]):
                print(f"       {player}: {score}")

        # Devam etmek istiyor mu?
        print("\n    " + "─" * 35)
        choice = input("    🔄 Başka bir tur oynamak ister misiniz? (E/H): ").strip().upper()

        if choice != 'E':
            break

    # Final sonuçları
    clear_screen()
    print_banner()
    print("    ╔═══════════════════════════════════╗")
    print("    ║       🏁 OYUN BİTTİ! 🏁           ║")
    print("    ╠═══════════════════════════════════╣")
    print(f"    ║   Toplam {round_num} tur oynandı           ║")
    print("    ╠═══════════════════════════════════╣")

    # Final sıralaması
    sorted_scores = sorted(total_scores.items(), key=lambda x: -x[1])

    medals = ["🥇", "🥈", "🥉"]
    for i, (player, score) in enumerate(sorted_scores):
        medal = medals[i] if i < 3 else "  "
        print(f"    ║  {medal} {player:13} : {score:4} puan   ║")

    print("    ╚═══════════════════════════════════╝")

    if sorted_scores:
        winner = sorted_scores[0][0]
        print(f"\n    🎊 Tebrikler {winner}! Oyunu kazandın! 🎊")

    print("\n    Oynadığınız için teşekkürler! 👋\n")

if __name__ == "__main__":
    main()
