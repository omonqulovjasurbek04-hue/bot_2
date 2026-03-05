from aiogram import Router, F
from aiogram.types import Message
from aiogram.filters import CommandStart
from aiogram.fsm.context import FSMContext
from keyboards import start_menu_kb, games_menu_kb, rps_kb, cancel_kb
from states import GameStates
from score import add_score, get_scores_text
import random

router = Router()

# /start → Bosh menyu
@router.message(CommandStart())
async def cmd_start(message: Message, state: FSMContext):
    await state.clear()
    await message.answer(
        "👋 Assalomu alaykum!\n\n"
        "🎮 *O'yinlar Botiga* xush kelibsiz!\n\n"
        "Quyidagi tugmalardan foydalaning:",
        parse_mode="Markdown",
        reply_markup=start_menu_kb()
    )

# 📊 Ballarim tugmasi
@router.message(F.text == "📊 Ballarim")
async def show_scores(message: Message):
    text = get_scores_text(message.from_user.id)
    await message.answer(text, parse_mode="Markdown", reply_markup=start_menu_kb())

# Bosh menyu tugmasi (start menyu)
@router.message(F.text == "🔙 Bosh menyu")
async def back_to_start(message: Message, state: FSMContext):
    await state.clear()
    await message.answer("🏠 Bosh menyudasiz.", reply_markup=start_menu_kb())

# Bot haqida
@router.message(F.text == "ℹ️ Bot haqida")
async def about_bot(message: Message):
    await message.answer(
        "🤖 *O'yinlar Boti*\n\n"
        "Bu botda 13 xil qiziqarli o'yin bor:\n"
        "🎮 Son topish\n"
        "✊ Tosh-Qaychi-Qog'oz\n"
        "🧮 Matematika\n"
        "🎲 Zar tashlash\n"
        "🔠 So'z o'yini\n"
        "❌⭕ Tic-Tac-Toe\n"
        "🔤 Hangman (Dor)\n"
        "🧩 Anagramma\n"
        "🎰 Slot mashinasi\n"
        "🤩 Emoji topish\n"
        "⌨️ Tez yoz!\n"
        "🧠 Xotira o'yini\n"
        "✅❌ Haqiqat/Yolg'on\n\n"
        "O'ynash uchun *🎮 O'yinlar* tugmasini bosing.",
        parse_mode="Markdown",
        reply_markup=start_menu_kb()
    )

# O'yinlar tugmasi → O'yinlar menyusi
@router.message(F.text == "🎮 O'yinlar")
async def show_games_menu(message: Message, state: FSMContext):
    await state.clear()
    await message.answer("🎮 O'yinni tanlang:", reply_markup=games_menu_kb())

# O'yinlar menyusiga qaytish
@router.message(F.text == "🔙 O'yinlar menyusi")
async def back_to_games(message: Message, state: FSMContext):
    await state.clear()
    await message.answer("🎮 O'yinni tanlang:", reply_markup=games_menu_kb())

# --- Son topish ---
@router.message(F.text == "🎮 Son topish")
async def start_guess_number(message: Message, state: FSMContext):
    number = random.randint(1, 100)
    await state.update_data(target_number=number, attempts=0)
    await state.set_state(GameStates.guess_number)
    await message.answer("Men 1 dan 100 gacha bo'lgan son o'yladim. Qani topishga harakat qiling!", reply_markup=cancel_kb())

@router.message(GameStates.guess_number)
async def process_guess(message: Message, state: FSMContext):
    if not message.text.isdigit():
        await message.answer("Iltimos, faqat son kiriting yoki menyuga qayting.")
        return
    
    guess = int(message.text)
    data = await state.get_data()
    target = data['target_number']
    attempts = data['attempts'] + 1
    
    if guess < target:
        await state.update_data(attempts=attempts)
        await message.answer("Kattaroq son ayting ⬆️")
    elif guess > target:
        await state.update_data(attempts=attempts)
        await message.answer("Kichikroq son ayting ⬇️")
    else:
        add_score(message.from_user.id, "son_topish")
        await message.answer(f"🎉 Tabriklayman! Siz sonni {attempts} ta urinishda topdingiz.\n+1 ⭐", reply_markup=games_menu_kb())
        await state.clear()

# --- Tosh-Qaychi-Qog'oz ---
@router.message(F.text == "✊✋✌️ Tosh-Qaychi-Qog'oz")
async def start_rps(message: Message, state: FSMContext):
    await state.set_state(GameStates.rps_game)
    await message.answer("Tosh, Qaychi yoki Qog'ozni tanlang:", reply_markup=rps_kb())

@router.message(GameStates.rps_game, F.text.in_(["✊ Tosh", "✋ Qog'oz", "✌️ Qaychi"]))
async def process_rps(message: Message, state: FSMContext):
    user_choice = message.text
    choices = ["✊ Tosh", "✋ Qog'oz", "✌️ Qaychi"]
    bot_choice = random.choice(choices)
    
    result = "Durang! 🤝"
    won = False
    if user_choice == "✊ Tosh":
        if bot_choice == "✌️ Qaychi": result = "Siz yutdingiz! 🎉"; won = True
        elif bot_choice == "✋ Qog'oz": result = "Men yutdim! 🤖"
    elif user_choice == "✋ Qog'oz":
        if bot_choice == "✊ Tosh": result = "Siz yutdingiz! 🎉"; won = True
        elif bot_choice == "✌️ Qaychi": result = "Men yutdim! 🤖"
    elif user_choice == "✌️ Qaychi":
        if bot_choice == "✋ Qog'oz": result = "Siz yutdingiz! 🎉"; won = True
        elif bot_choice == "✊ Tosh": result = "Men yutdim! 🤖"
        
    if won:
        add_score(message.from_user.id, "tosh_qaychi")
        result += "\n+1 ⭐"
    await message.answer(f"Siz: {user_choice}\nMen: {bot_choice}\n\nNatija: {result}", reply_markup=games_menu_kb())
    await state.clear()

@router.message(GameStates.rps_game)
async def process_rps_invalid(message: Message):
    await message.answer("Iltimos, pastdagi tugmalardan birini tanlang:")

# --- Matematika ---
@router.message(F.text == "🧮 Matematika")
async def start_math(message: Message, state: FSMContext):
    num1 = random.randint(1, 100)
    num2 = random.randint(1, 100)
    op = random.choice(['+', '-', '*'])
    
    if op == '+': ans = num1 + num2
    elif op == '-': ans = num1 - num2
    else: ans = num1 * num2
    
    await state.update_data(answer=ans)
    await state.set_state(GameStates.math_quiz)
    await message.answer(f"Yechishga harakat qiling:\n\n{num1} {op} {num2} = ?", reply_markup=cancel_kb())

@router.message(GameStates.math_quiz)
async def process_math(message: Message, state: FSMContext):
    if not (message.text.isdigit() or (message.text.startswith('-') and message.text[1:].isdigit())):
        await message.answer("Iltimos, faqat son kiriting (javob).")
        return
        
    user_ans = int(message.text)
    data = await state.get_data()
    correct_ans = data['answer']
    
    if user_ans == correct_ans:
        add_score(message.from_user.id, "matematika")
        await message.answer("✅ Qoyil, to'g'ri topdingiz!\n+1 ⭐", reply_markup=games_menu_kb())
    else:
        await message.answer(f"❌ Noto'g'ri. To'g'ri javob: {correct_ans} edi.", reply_markup=games_menu_kb())
        
    await state.clear()


import asyncio
import time
from aiogram.enums import DiceEmoji

# --- Zar tashlash ---
@router.message(F.text == "🎲 Zar tashlash")
async def start_dice(message: Message, state: FSMContext):
    await message.answer("Men ham, siz ham bittadan zar 🎲 tashlaymiz. Kimning zali ko'p tushsa o'sha yutadi!\nBirinchi men tashlayman:")
    await asyncio.sleep(1)
    
    bot_msg = await message.answer_dice(emoji=DiceEmoji.DICE)
    bot_value = bot_msg.dice.value
    
    await asyncio.sleep(4) # Animatsiya uchun vaqt
    await message.answer(f"Menda {bot_value} tushdi. Endi sizning navbatingiz!\nChatga 🎲 emojisini yuboring.", reply_markup=cancel_kb())
    await state.update_data(bot_dice=bot_value)
    await state.set_state(GameStates.dice_game)

@router.message(GameStates.dice_game)
async def process_dice(message: Message, state: FSMContext):
    if not message.dice or message.dice.emoji != "🎲":
        await message.answer("Iltimos, 🎲 emojisini jo'nating!")
        return
        
    user_value = message.dice.value
    data = await state.get_data()
    bot_value = data['bot_dice']
    
    await asyncio.sleep(4)
    
    if user_value > bot_value:
        res = "Siz yutdingiz! 🎉\n+1 ⭐"
        add_score(message.from_user.id, "zar_tashlash")
    elif user_value < bot_value:
        res = "Men yutdim! 🤖"
    else:
        res = "Durang! 🤝"
        
    await message.answer(f"Natija: {res}", reply_markup=games_menu_kb())
    await state.clear()

# --- Emoji topish ---
EMOJI_GAMES = [
    {"emojis": "🍎 🚗 🐶 ⚽", "correct": "🍎", "question": "Qaysi biri meva?"},
    {"emojis": "💻 🎸 📱 ⌚", "correct": "🎸", "question": "Qaysi biri musiqa asbobi?"},
    {"emojis": "🦁 🐯 🐘 🐱", "correct": "🐱", "question": "Qaysi biri uy hayvoni?"},
    {"emojis": "⚽ 🏀 🎾 🎮", "correct": "🎮", "question": "Qaysi biri elektron o'yin?"},
    {"emojis": "🍔 🥗 🍟 🍕", "correct": "🥗", "question": "Qaysi biri sog'lom ovqat?"}
]

@router.message(F.text == "🤩 Emoji topish")
async def start_emoji_game(message: Message, state: FSMContext):
    game = random.choice(EMOJI_GAMES)
    
    from aiogram.types import ReplyKeyboardMarkup, KeyboardButton
    emojis_list = game["emojis"].split(" ")
    random.shuffle(emojis_list)
    
    kb = ReplyKeyboardMarkup(
        keyboard=[[KeyboardButton(text=e) for e in emojis_list], [KeyboardButton(text="🔙 Bosh menyu")]],
        resize_keyboard=True
    )
    
    await state.update_data(correct_emoji=game["correct"])
    await state.set_state(GameStates.emoji_guess)
    await message.answer(f"Savol: {game['question']}\n\nQuyidagi emojilardan to'g'risini tanlang:", reply_markup=kb)

@router.message(GameStates.emoji_guess)
async def process_emoji_guess(message: Message, state: FSMContext):
    data = await state.get_data()
    correct = data['correct_emoji']
    
    if message.text == correct:
        add_score(message.from_user.id, "emoji_topish")
        await message.answer("✅ To'g'ri topdingiz!\n+1 ⭐", reply_markup=games_menu_kb())
    else:
        await message.answer(f"❌ Noto'g'ri! To'g'ri javob: {correct} edi.", reply_markup=games_menu_kb())
        
    await state.clear()


# --- Tez yoz (Typing Game) ---
WORDS_TO_TYPE = [
    "olma anor uzum gilos",
    "bugun havo juda yaxshi",
    "men dasturlashni yaxshi bilaman",
    "toshkent juda chiroyli shahar",
    "telegram bot yozish oson",
]

@router.message(F.text == "⌨️ Tez yoz!")
async def start_typing_game(message: Message, state: FSMContext):
    sentence = random.choice(WORDS_TO_TYPE)
    
    # Avval matnni ko'rsatamiz
    await message.answer(f"👇 Quyidagi matnni XUDDI SHUNDAY yozib yuboring:\n\n📝 {sentence}", reply_markup=cancel_kb())
    
    # Vaqtni shu paytdan boshlaymiz
    start_time = time.time()
    await state.update_data(sentence=sentence, start_time=start_time)
    await state.set_state(GameStates.typing_game)

@router.message(GameStates.typing_game)
async def process_typing_game(message: Message, state: FSMContext):
    data = await state.get_data()
    correct_sentence = data['sentence']
    start_time = data['start_time']
    
    end_time = time.time()
    time_taken = round(end_time - start_time, 2)
    
    if message.text == correct_sentence:
        add_score(message.from_user.id, "tez_yoz")
        if time_taken < 5.0:
            rating = "🔥 Dahshat tez!"
        elif time_taken < 10.0:
            rating = "👍 Yaxshi natija!"
        else:
            rating = "🐢 Biroz sekinsiz, yanada tezroq harakat qiling."
            
        await message.answer(f"✅ Qoyil! Siz matnni xatosiz yozdingiz.\n+1 ⭐\n\n⏱ Sarflangan vaqt: {time_taken} soniya\nBaho: {rating}", reply_markup=games_menu_kb())
    else:
        await message.answer(f"❌ Xato yozdingiz!\n\nSiz yozdingiz: {message.text}\nKerak edi: {correct_sentence}\n\nQayta urinib ko'rish uchun menyudan tanlang.", reply_markup=games_menu_kb())
        
    await state.clear()


# --- Slot mashinasi ---
@router.message(F.text == "🎰 Slot mashinasi")
async def start_slot(message: Message, state: FSMContext):
    await message.answer("Omadingizni sinab ko'ramiz! 🎰 tashlayapman...")
    await asyncio.sleep(1)
    
    bot_msg = await message.answer_dice(emoji=DiceEmoji.SLOT_MACHINE)
    val = bot_msg.dice.value
    
    await asyncio.sleep(3)
    
    # Telegram slot mashinasida 1, 22, 43, 64 raqamlari katta yutuqlarni bildiradi
    # 64 raqami bu 7-7-7 (Jackpot)
    if val == 64:
        res = "🎰 JACKPOT!!! TABRIKLAYMIZ! 🎉🎉🎉\n+1 ⭐"
        add_score(message.from_user.id, "slot")
    elif val in [1, 22, 43]:
        res = "Yaxshi yutuq! 💰\n+1 ⭐"
        add_score(message.from_user.id, "slot")
    else:
        res = "Afsuski, omad kulib boqmadi. Yana urinib ko'ring! 😞"
        
    await message.answer(res, reply_markup=games_menu_kb())

# --- Anagramma ---
ANAGRAM_WORDS = ["olma", "kitob", "dastur", "telefon", "maktab", "mashina"]

@router.message(F.text == "🧩 Anagramma")
async def start_anagram(message: Message, state: FSMContext):
    word = random.choice(ANAGRAM_WORDS)
    shuffled = list(word)
    random.shuffle(shuffled)
    shuffled_str = "".join(shuffled)
    
    await state.update_data(word=word)
    await state.set_state(GameStates.anagram)
    
    await message.answer(f"Ushbu harflardan qanday so'z yasalgan?\n\n🔠 **{shuffled_str.upper()}**", parse_mode="Markdown", reply_markup=cancel_kb())

@router.message(GameStates.anagram)
async def process_anagram(message: Message, state: FSMContext):
    data = await state.get_data()
    correct_word = data['word']
    
    if message.text.lower() == correct_word:
        add_score(message.from_user.id, "anagramma")
        await message.answer("✅ Qoyil! To'g'ri topdingiz.\n+1 ⭐", reply_markup=games_menu_kb())
    else:
        await message.answer(f"❌ Noto'g'ri.\nTo'g'ri javob: *{correct_word.upper()}* edi.", parse_mode="Markdown", reply_markup=games_menu_kb())
        
    await state.clear()

# --- Dor o'yini (Hangman) ---
HANGMAN_WORDS = ["kompyuter", "internet", "dasturchi", "algoritm", "klaviatura"]

@router.message(F.text == "🔤 Hangman (Dor)")
async def start_hangman(message: Message, state: FSMContext):
    word = random.choice(HANGMAN_WORDS)
    guessed = ["_"] * len(word)
    attempts = 5
    
    await state.update_data(word=word, guessed=guessed, attempts=attempts)
    await state.set_state(GameStates.hangman)
    
    await message.answer(f"So'zni toping ({len(word)} ta harf):\n\n`{' '.join(guessed)}`\n\nSizda {attempts} ta imkoniyat bor. Harf yuboring:", parse_mode="MarkdownV2", reply_markup=cancel_kb())

@router.message(GameStates.hangman)
async def process_hangman(message: Message, state: FSMContext):
    letter = message.text.lower()
    
    if len(letter) != 1 or not letter.isalpha():
        await message.answer("Iltimos, faqat bitta harf yuboring!")
        return
        
    data = await state.get_data()
    word = data['word']
    guessed = data['guessed']
    attempts = data['attempts']
    
    if letter in word:
        for i, char in enumerate(word):
            if char == letter:
                guessed[i] = letter
        
        if "_" not in guessed:
            add_score(message.from_user.id, "hangman")
            await message.answer(f"🎉 Tabriklayman! Siz so'zni topdingiz: {word.capitalize()}\n+1 ⭐", reply_markup=games_menu_kb())
            await state.clear()
            return
            
        await state.update_data(guessed=guessed)
        await message.answer(f"✅ To'g'ri!\n\n`{' '.join(guessed)}`\n\nQolgan imkoniyatlar: {attempts}", parse_mode="MarkdownV2", reply_markup=cancel_kb())
    else:
        attempts -= 1
        if attempts <= 0:
            await message.answer(f"💀 Urunishlar tugadi. Yutqazdingiz!\n\nYashiringan so'z: *{word.capitalize()}* edi.", parse_mode="Markdown", reply_markup=games_menu_kb())
            await state.clear()
            return
            
        await state.update_data(attempts=attempts)
        await message.answer(f"❌ Noto'g'ri!\n\n`{' '.join(guessed)}`\n\nQolgan imkoniyatlar: {attempts}", parse_mode="MarkdownV2", reply_markup=cancel_kb())

# --- Tic-Tac-Toe (X va O) ---
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton, CallbackQuery

def tictactoe_kb(board: list):
    keyboard = []
    for i in range(3):
        row = []
        for j in range(3):
            val = board[i*3 + j]
            text = " " if val == "" else val
            row.append(InlineKeyboardButton(text=text, callback_data=f"ttt_{i*3+j}"))
        keyboard.append(row)
    return InlineKeyboardMarkup(inline_keyboard=keyboard)

@router.message(F.text == "❌⭕ Tic-Tac-Toe")
async def start_tictactoe(message: Message, state: FSMContext):
    board = [""] * 9
    await state.update_data(board=board, turn="❌")
    await state.set_state(GameStates.tictactoe)
    await message.answer("Tic-Tac-Toe o'yini boshlandi! Siz ❌ siz.", reply_markup=tictactoe_kb(board))
    await message.answer("Orqaga qaytish uchun:", reply_markup=cancel_kb())

def check_winner(board):
    win_lines = [(0,1,2), (3,4,5), (6,7,8), (0,3,6), (1,4,7), (2,5,8), (0,4,8), (2,4,6)]
    for a, b, c in win_lines:
        if board[a] and board[a] == board[b] == board[c]:
            return board[a]
    if "" not in board:
        return "Durang"
    return None

@router.callback_query(F.data.startswith("ttt_"), GameStates.tictactoe)
async def process_tictactoe(callback: CallbackQuery, state: FSMContext):
    pos = int(callback.data.split("_")[1])
    data = await state.get_data()
    board = data['board']
    turn = data['turn']
    
    if board[pos] != "":
        await callback.answer("Bu joy band!", show_alert=True)
        return
        
    board[pos] = turn
    winner = check_winner(board)
    
    if winner:
        if winner == "Durang":
            res_text = "Durang! 🤝"
        else:
            res_text = f"G'olib: {winner} 🎉"
            if winner == "❌":
                add_score(callback.from_user.id, "tictactoe")
                res_text += "\n+1 ⭐"
        await callback.message.edit_text(res_text, reply_markup=tictactoe_kb(board))
        await callback.answer()
        await state.clear()
        return
        
    # Bot moves (random empty spot)
    empty_spots = [i for i, x in enumerate(board) if x == ""]
    if empty_spots:
        bot_pos = random.choice(empty_spots)
        board[bot_pos] = "⭕"
        
    winner = check_winner(board)
    if winner:
        if winner == "Durang":
            res_text = "Durang! 🤝"
        else:
            res_text = f"G'olib: {winner} 🎉"
        await callback.message.edit_text(res_text, reply_markup=tictactoe_kb(board))
        await state.clear()
    else:
        await state.update_data(board=board)
        await callback.message.edit_text("Sizning navbatingiz (Siz ❌):", reply_markup=tictactoe_kb(board))
        
    await callback.answer()

# --- So'z o'yini ---
import string

@router.message(F.text == "🔠 So'z o'yini")
async def start_word_chain(message: Message, state: FSMContext):
    await state.update_data(used_words=[])
    await state.set_state(GameStates.word_chain)
    
    start_word = "olma"
    await state.update_data(used_words=[start_word])
    await message.answer(f"O'yinni men boshladim: *{start_word.capitalize()}*\n\nEndi siz '{start_word[-1].upper()}' harfiga so'z ayting (Faqat bitta so'z yuboring).", parse_mode="Markdown", reply_markup=cancel_kb())

@router.message(GameStates.word_chain)
async def process_word_chain(message: Message, state: FSMContext):
    user_word = message.text.lower().strip()
    
    if not user_word.isalpha():
        await message.answer("Iltimos, faqat harflardan iborat yagona so'z yuboring.")
        return
        
    data = await state.get_data()
    used_words = data['used_words']
    last_word = used_words[-1]
    last_char = last_word[-1]
    
    if user_word[0] != last_char:
        await message.answer(f"❌ So'z '{last_char.upper()}' harfi bilan boshlanishi kerak!\n\nDavom etishdan bosh tortsangiz menyuga qayting.", reply_markup=cancel_kb())
        return
        
    if user_word in used_words:
        await message.answer(f"Ayyorlik qilmang, '{user_word}' so'zi oldin aytilgan! Boshqa so'z toping.", reply_markup=cancel_kb())
        return
        
    used_words.append(user_word)
    
    # Bot random response (simple mock logic)
    bot_letters = ['a', 'b', 'd', 'e', 'g', 'i', 'k', 'l', 'm', 'n', 'o', 'p', 'r', 's', 't', 'u', 'v', 'y', 'z', 'sh', 'ch']
    next_start = user_word[-1]
    
    if next_start not in bot_letters:
        add_score(message.from_user.id, "soz_oyini")
        await message.answer(f"🎉 Siz meni yengdingiz! '{next_start.upper()}' ga boshlanadigan so'z bilmayman.\n+1 ⭐", reply_markup=games_menu_kb())
        await state.clear()
        return
        
    # Just a mock bot logic generating fake valid word or some preset words
    preset_dict = {
        'a': 'anor', 'b': 'bahor', 'd': 'daraxt', 'e': 'elak', 'g': 'gul', 'i': 'ilon', 
        'k': 'kitob', 'l': 'lola', 'm': 'maktab', 'n': 'non', 'o': 'ozuq', 'p': 'palov',
        'r': 'rasm', 's': 'sartarosh', 't': 'tog', 'u': 'uzum', 'v': 'vaqt', 'y': 'yoz', 'z': 'zamon'
    }
    
    bot_word = preset_dict.get(next_start, next_start + "a") # Fallback to a fake word
    
    while bot_word in used_words:
         bot_word = bot_word + "a" # Prevent duplicate
         if len(bot_word) > 10: # Failsafe
            add_score(message.from_user.id, "soz_oyini")
            await message.answer("Siz yutdingiz! Boshqa so'z topa olmadim.\n+1 ⭐", reply_markup=games_menu_kb())
            await state.clear()
            return

    used_words.append(bot_word)
    await state.update_data(used_words=used_words)
    
    await message.answer(f"Bot aytgan so'z: *{bot_word.capitalize()}*\nEndi siz '{bot_word[-1].upper()}' harfiga ayting.", parse_mode="Markdown", reply_markup=cancel_kb())


from keyboards_extra import truth_false_kb

# --- Haqiqat yoki Yolg'on ---
TF_QUESTIONS = [
    {"q": "Suv H2O tarkibiga ega.", "a": "✅ Haqiqat"},
    {"q": "O'rgimchaklarda 6 ta oyoq bor.", "a": "❌ Yolg'on"},  # 8 ta oyoq
    {"q": "O'zbekistonning poytaxti Toshkent.", "a": "✅ Haqiqat"},
    {"q": "Quyosh Yerdan kichikroq.", "a": "❌ Yolg'on"},
    {"q": "Dunyodagi eng katta okean bu Tinch okeani.", "a": "✅ Haqiqat"},
    {"q": "Pingvinlarucha oladi.", "a": "❌ Yolg'on"},
    {"q": "Python dasturlash tili nomini ilondan olgan.", "a": "❌ Yolg'on"}, # Monty Python's Flying Circus
]

@router.message(F.text == "✅❌ Haqiqat/Yolg'on")
async def start_truth_false(message: Message, state: FSMContext):
    question = random.choice(TF_QUESTIONS)
    
    await state.update_data(correct_answer=question["a"])
    await state.set_state(GameStates.truth_false)
    
    await message.answer(f"Ushbu gap haqiqatmi yoki yolg'on?\n\n💬: *{question['q']}*", parse_mode="Markdown", reply_markup=truth_false_kb())

@router.message(GameStates.truth_false, F.text.in_(["✅ Haqiqat", "❌ Yolg'on"]))
async def process_truth_false(message: Message, state: FSMContext):
    data = await state.get_data()
    correct = data['correct_answer']
    
    if message.text == correct:
        add_score(message.from_user.id, "haqiqat_yolgon")
        await message.answer("✅ To'g'ri topdingiz!\n+1 ⭐", reply_markup=games_menu_kb())
    else:
        await message.answer(f"❌ Noto'g'ri!\nTo'g'ri javob: {correct} edi.", reply_markup=games_menu_kb())
        
    await state.clear()


# --- Xotira o'yini ---
@router.message(F.text == "🧠 Xotira o'yini")
async def start_memory_game(message: Message, state: FSMContext):
    # 5 ta ketma-ket tasodifiy son
    numbers = [str(random.randint(0, 9)) for _ in range(5)]
    sequence = " ".join(numbers)
    
    msg = await message.answer(f"Yodlab qoling, faqat 3 soniya vaqtingiz bor!\n\n🔢 **{sequence}**", parse_mode="Markdown")
    
    await state.update_data(sequence=sequence)
    await state.set_state(GameStates.memory_game)
    
    await asyncio.sleep(3)
    
    # Xabarni yashirish / o'zgartirish
    try:
        await msg.edit_text("Sonlar yashirildi! Qo'lingizdan kelganicha eslab, ketma-ketlikda yozib yuboring (bo'sh joylarsiz yoki bo'sh joy bilan):")
    except:
        pass # If message edit fails
        
    await message.answer("Yodingizda qolgan sonlarni yuboring:", reply_markup=cancel_kb())

@router.message(GameStates.memory_game)
async def process_memory_game(message: Message, state: FSMContext):
    data = await state.get_data()
    correct_sequence = data['sequence']
    
    # O'yinchining javobini formatlash (probellarni olib tashlash)
    user_ans = message.text.replace(" ", "")
    correct_ans = correct_sequence.replace(" ", "")
    
    if user_ans == correct_ans:
        add_score(message.from_user.id, "xotira")
        await message.answer("🎉 A'lo xotira! Barcha sonlarni to'g'ri topdingiz.\n+1 ⭐", reply_markup=games_menu_kb())
    else:
        await message.answer(f"❌ Xato! Siz {user_ans} dedingiz.\n\nTo'g'ri ketma-ketlik: **{correct_sequence}** edi.", parse_mode="Markdown", reply_markup=games_menu_kb())
        
    await state.clear()
