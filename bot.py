import asyncio
import logging
import sys
from os import getenv
from typing import Any, Dict

from aiogram import Bot, Dispatcher, F, Router, html
from aiogram.enums import ParseMode
from aiogram.filters import Command, CommandStart
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
from aiogram.types import (
    KeyboardButton,
    Message,
    ReplyKeyboardMarkup,
    ReplyKeyboardRemove,
)

import numpy as np
import matplotlib.pyplot as plt
import matplotlib.colors as mcolors

from config import token, Form, Buttons, questions
import matplotlib.pyplot as plt

# Bot token can be obtained via https://t.me/BotFather
TOKEN = token
form_router = Router()
# All handlers should be attached to the Router (or Dispatcher)
bot = Bot(token=TOKEN)

i = 1
counter = 0

@form_router.message(CommandStart())
async def command_start(message: Message, state: FSMContext) -> None:
    global i
    global counter
    i = 1
    await state.set_state(Form.start)
    await message.answer(
        "Привет, желаете пройти тест на тревожность по шкале Бека?",
        reply_markup=ReplyKeyboardRemove(),
    )


@form_router.message(Command("cancel"))
@form_router.message(F.text.casefold() == "cancel")
async def cancel_handler(message: Message, state: FSMContext) -> None:
    """
    Allow user to cancel any action
    """
    current_state = await state.get_state()
    if current_state is None:
        return

    logging.info("Cancelling state %r", current_state)
    await state.clear()
    await message.answer(
        "Cancelled.",
        reply_markup=ReplyKeyboardRemove(),
    )




@form_router.message(Form.start)
async def process_name(message: Message, state: FSMContext) -> None:
    global counter
    if message.text == "Слегка. Не слишком меня беспокоит":
        counter+=1
        await state.update_data(value=counter)
    elif message.text == "Умеренно. Это было неприятно, но я могу это перенести":
        counter += 2
        await state.update_data(value=counter)
    elif message.text == "Очень сильно. Я с трудом могу это переносить":
        counter += 3
    else:
        pass
    await state.set_state(getattr(Form, f"q{i}"))
    await message.answer(
        "Я буду приводить список симптомов, твоя задача оценить, насколько они тебя беспокоят",
        reply_markup=ReplyKeyboardMarkup(
            keyboard=[
                [
                    KeyboardButton(text=f"Понятно"),

                ]
            ],
            resize_keyboard=True,
        ),
    )

def set_next_question_state(state: FSMContext) -> None:
    global i
    if i<21:
        state.set_state(getattr(Form, f"q{i}"))
    else:
        state.set_state(Form.results)
        i=0
    i+=1


@form_router.message(getattr(Form, f"q{i}"))
async def process_test(message: Message, state: FSMContext) -> None:
    global i
    global counter
    if message.text == "Слегка. Не слишком меня беспокоит":
        counter+=1
        await state.update_data(value=counter)
    elif message.text == "Умеренно. Это было неприятно, но я могу это перенести":
        counter += 2
        await state.update_data(value=counter)
    elif message.text == "Очень сильно. Я с трудом могу это переносить":
        counter += 3
    else:
        pass

    await message.answer(
        text=questions[i],
        reply_markup=ReplyKeyboardMarkup(
            keyboard=[
                [
                    Buttons.anwser0,
                    Buttons.anwser1,
                    Buttons.anwser2,
                    Buttons.anwser3

                ]
            ],
            resize_keyboard=True,
        ),
    )
    if i == 21:
        await state.set_state(Form.results)
        i = 1
    else:
        set_next_question_state(state)


def print_pic(val) -> None:

    x = np.linspace(0, 63, 100)
    y = np.zeros_like(x)

    # Создание градиента от зеленого до красного
    colors = mcolors.LinearSegmentedColormap.from_list('g_to_r', ['green', 'red'])

    # Построение графика
    plt.figure(figsize=(8, 2))
    plt.scatter(x, y, c=x, cmap=colors, s=100)

    tick_values = [0, 22, 36, 63]

    plt.xticks(tick_values)
    plt.yticks([])
    # Установка пределов оси X
    plt.xlim(0, 63)
    plt.title('Шкала тревожности Бекка')
    plt.axvline(x=val, color='black', linestyle='--')  # Размещение вертикальной полоски
    # Сохранение графика в виде изображения
    filename = "graph.png"
    plt.savefig(filename)



@form_router.message(Form.results)
async def process_res(message: Message, state: FSMContext) -> None:
    global counter
    data = await state.get_data()
    val = data.get("value")
    await state.set_state(Form.picture)
    await message.answer(
      f"Ваши результаты готовы: вы набрали {val}",
        reply_markup=ReplyKeyboardMarkup(
            keyboard=[
                [
                    KeyboardButton(text=f"Расшифровка"),

                ]
            ],
            resize_keyboard=True,
        ),
    )
    counter=val

scale = [0, 21, 22, 35, 36, 63]
def prp(val):
    out = " "
    for i in scale:
        if val<=21:
            txt = 'Cупер результат! У вас низкая тревожность\n'

            print(out)
            for i in scale:
                if i==1 or i==21:
                    c= f"{i}  {val}Вы{val} "
                    out = out + c


        elif val<=35 and val>=22:
            txt = 'Не очень радужно( Это средний уровень тревожности\n'

            print(out)
            for i in scale:
                if i == 22 or i == 35:
                    c = f"{i}-  {val}Вы{val} -"
                    out =out + c
        else:
            txt = 'Плохие новости(( Это высокий уровень. Пожалуйста, обратитесь к специалисту и берегите себя!\n'
            print(out)
            for i in scale:
                if i == 36 or i == 63:
                    c = f"{i}-  {val}Вы{val} -"
                    out = out + c
                    out = out + "\n Сайт для Вас: https://netaktrevozhno.tilda.ws/"
        return txt + out


@form_router.message(Form.picture)
async def process_pic(message: Message, state: FSMContext) -> None:
    global counter
    out = prp(counter)
    await state.set_state(Form.picture)
    await message.answer(
        f"{out}",
        reply_markup=ReplyKeyboardMarkup(
            keyboard=[
                [
                    KeyboardButton(text=f"Пройти заново"),

                ]
            ],
            resize_keyboard=True,
        ),
    )
    counter=0
    await state.set_state(Form.start)

async def show_summary(message: Message, data: Dict[str, Any], positive: bool = True) -> None:
    name = data["name"]
    language = data.get("language", "<something unexpected>")
    text = f"I'll keep in mind that, {html.quote(name)}, "
    text += (
        f"you like to write bots with {html.quote(language)}."
        if positive
        else "you don't like to write bots, so sad..."
    )
    await message.answer(text=text, reply_markup=ReplyKeyboardRemove())


async def main():
    bot = Bot(token=TOKEN, parse_mode=ParseMode.HTML)
    dp = Dispatcher()
    dp.include_router(form_router)

    await dp.start_polling(bot)


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO, stream=sys.stdout)
    asyncio.run(main())