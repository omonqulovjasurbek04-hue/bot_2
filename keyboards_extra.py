from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

def truth_false_kb():
    return ReplyKeyboardMarkup(
        keyboard=[
            [KeyboardButton(text="✅ Haqiqat"), KeyboardButton(text="❌ Yolg'on")],
            [KeyboardButton(text="🔙 Bosh menyu")]
        ],
        resize_keyboard=True
    )
