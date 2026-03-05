from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

# /start bosilganda chiqadigan bosh menyu
def start_menu_kb():
    return ReplyKeyboardMarkup(
        keyboard=[
            [KeyboardButton(text="🎮 O'yinlar")],
            [KeyboardButton(text="📊 Ballarim"), KeyboardButton(text="ℹ️ Bot haqida")]
        ],
        resize_keyboard=True
    )

# O'yinlar tugmasini bosganda chiqadigan o'yinlar menyusi
def games_menu_kb():
    return ReplyKeyboardMarkup(
        keyboard=[
            [KeyboardButton(text="🎮 Son topish"), KeyboardButton(text="✊✋✌️ Tosh-Qaychi-Qog'oz")],
            [KeyboardButton(text="🧮 Matematika"), KeyboardButton(text="🎲 Zar tashlash")],
            [KeyboardButton(text="🔠 So'z o'yini"), KeyboardButton(text="❌⭕ Tic-Tac-Toe")],
            [KeyboardButton(text="🔤 Hangman (Dor)"), KeyboardButton(text="🧩 Anagramma")],
            [KeyboardButton(text="🎰 Slot mashinasi"), KeyboardButton(text="🤩 Emoji topish")],
            [KeyboardButton(text="⌨️ Tez yoz!"), KeyboardButton(text="🧠 Xotira o'yini")],
            [KeyboardButton(text="✅❌ Haqiqat/Yolg'on")],
            [KeyboardButton(text="🔙 Bosh menyu")]
        ],
        resize_keyboard=True
    )

def rps_kb():
    return ReplyKeyboardMarkup(
        keyboard=[
            [KeyboardButton(text="✊ Tosh"), KeyboardButton(text="✋ Qog'oz"), KeyboardButton(text="✌️ Qaychi")],
            [KeyboardButton(text="🔙 O'yinlar menyusi")]
        ],
        resize_keyboard=True
    )
    
def cancel_kb():
    return ReplyKeyboardMarkup(
        keyboard=[
            [KeyboardButton(text="🔙 O'yinlar menyusi")]
        ],
        resize_keyboard=True
    )
