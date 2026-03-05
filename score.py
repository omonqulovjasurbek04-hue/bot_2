import json
import os

SCORE_FILE = os.path.join(os.path.dirname(__file__), "user.json")

GAME_KEYS = [
    "son_topish", "tosh_qaychi", "matematika", "zar_tashlash",
    "soz_oyini", "tictactoe", "hangman", "anagramma",
    "slot", "emoji_topish", "tez_yoz", "xotira", "haqiqat_yolgon"
]

GAME_NAMES = {
    "son_topish": "🎮 Son topish",
    "tosh_qaychi": "✊ Tosh-Qaychi-Qog'oz",
    "matematika": "🧮 Matematika",
    "zar_tashlash": "🎲 Zar tashlash",
    "soz_oyini": "🔠 So'z o'yini",
    "tictactoe": "❌⭕ Tic-Tac-Toe",
    "hangman": "🔤 Hangman",
    "anagramma": "🧩 Anagramma",
    "slot": "🎰 Slot mashinasi",
    "emoji_topish": "🤩 Emoji topish",
    "tez_yoz": "⌨️ Tez yoz",
    "xotira": "🧠 Xotira o'yini",
    "haqiqat_yolgon": "✅❌ Haqiqat/Yolg'on",
}


def _load_data() -> dict:
    if os.path.exists(SCORE_FILE):
        with open(SCORE_FILE, "r", encoding="utf-8") as f:
            return json.load(f)
    return {}


def _save_data(data: dict):
    with open(SCORE_FILE, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)


def _get_user(user_id: int) -> dict:
    data = _load_data()
    uid = str(user_id)
    if uid not in data:
        data[uid] = {key: 0 for key in GAME_KEYS}
        _save_data(data)
    return data[uid]


def add_score(user_id: int, game_key: str, points: int = 1):
    """O'yin yutilganda ball qo'shish"""
    data = _load_data()
    uid = str(user_id)
    if uid not in data:
        data[uid] = {key: 0 for key in GAME_KEYS}
    if game_key not in data[uid]:
        data[uid][game_key] = 0
    data[uid][game_key] += points
    _save_data(data)


def get_scores_text(user_id: int) -> str:
    """Foydalanuvchining barcha ballarini matn ko'rinishida qaytarish"""
    user = _get_user(user_id)
    total = sum(user.values())
    
    lines = ["📊 *Sizning ballaringiz:*\n"]
    for key in GAME_KEYS:
        name = GAME_NAMES.get(key, key)
        score = user.get(key, 0)
        if score > 0:
            lines.append(f"{name}: *{score}* ball")
    
    if total == 0:
        lines.append("Hali ball yig'ilmagan. O'ynab ko'ring!")
    
    lines.append(f"\n🏆 *Umumiy: {total} ball*")
    return "\n".join(lines)
