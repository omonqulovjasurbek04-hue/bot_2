from aiogram.fsm.state import State, StatesGroup

class GameStates(StatesGroup):
    guess_number = State()
    math_quiz = State()
    rps_game = State()
    dice_game = State()        # 1. Zar tashlash
    word_chain = State()       # 2. So'z o'yini
    tictactoe = State()        # 3. Tic-Tac-Toe
    hangman = State()          # 4. Dor o'yini
    anagram = State()          # 5. Anagramma
    slot_machine = State()     # 7. Slot mashinasi
    emoji_guess = State()      # 8. Emoji topish
    typing_game = State()      # 9. Tez yoz
    truth_false = State()      # 11. Haqiqat yoki yolg'on
    memory_game = State()      # 12. Xotira o'yini
