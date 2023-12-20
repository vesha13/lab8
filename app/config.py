from enum import Enum
from aiogram.fsm.state import State, StatesGroup
from aiogram.types import KeyboardButton

token = "6553358739:AAF5ya6dHBbQvoxpmwiieh8GGifMtI3N6B4"
db_file = "database.vdb"

CURRENT_STATE = "CURRENT_STATE"

class Form(StatesGroup):
    start = State()
    results = State()
    picture = State()
    for i in range(1, 22):
        locals()[f'q{i}'] = State()

print(Form.q2, Form.q1)
question_state = getattr(Form, f"q{2}")
print(question_state)
class Buttons():
    anwser0 = KeyboardButton(text="Совсем не беспокоит")
    anwser1= KeyboardButton(text="Слегка. Не слишком меня беспокоит")
    anwser2 = KeyboardButton(text="Умеренно. Это было неприятно, но я могу это перенести")
    anwser3 = KeyboardButton(text="Очень сильно. Я с трудом могу это переносить")
    back = KeyboardButton(text="Назад")



questions=[
        " ",
        "Ощущение онемении или покалывания в теле",
        "Ощущение жары",
        "Дрожь в ногах",
        "Неспособность расслабиться",
        "Страх, что произойдет самое плохое",
        "Головокружение или ощущение легкости в голове",
        "Ускоренное сердцебиение",
        "Неустойчивость",
        "Ощущение ужаса",
        "Нервозность",
        "Дрожь в руках",
        "Ощущение удушья",
        "Шаткость походки",
        "Страх утраты контроля",
        "Затрудненность дыхания",
        "Страх смерти",
        "Испуг",
        "Желудочно-кишечные расстройства",
        "Обмороки",
        "Приливы крови к лицу",
        "Усиление потоотделения (не связанное с жарой)"
           ]