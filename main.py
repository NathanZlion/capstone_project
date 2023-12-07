import asyncio
import sys
import logging

from os import getenv
from aiogram import Bot, Dispatcher, F, Router, html
from aiogram.enums import ParseMode
from aiogram.filters import Command, CommandStart
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import StatesGroup, State
from aiogram.types import (
    InlineKeyboardButton,
    KeyboardButton,
    Message,
    ReplyKeyboardMarkup,
    ReplyKeyboardRemove,
)

from aiogram.utils.keyboard import InlineKeyboardBuilder
from dotenv import load_dotenv
from database_handler import DB_Handler


load_dotenv(".env")
BOT_TOKEN = getenv("BOT_TOKEN")

form_router = Router()
db_handler = None


class Form(StatesGroup):
    name = State()
    phone_number = State()
    role = State()


@form_router.message(CommandStart())
async def command_start(message: Message, state: FSMContext) -> None:
    """checks if the user has already been registered in the database"""
    user_id = message.from_user.id

    # check user in database
    user_in_database = True

    if user_in_database:
        await state.set_state(Form.name)
        await message.answer(
            "Hi there, Welcome to Ride Hailing Bot. What's your name?",
            reply_markup=ReplyKeyboardRemove(),
        )

    else:
        await state.set_state(Form.name)
        await message.answer(
            "Hi there, Welcome to Ride Hailing Bot. What's your name?",
            reply_markup=ReplyKeyboardRemove(),
        )


@form_router.message(Form.name)
async def process_name(message: Message, state: FSMContext) -> None:
    user_input: str = message.text
    if len(user_input.split()) != 2:
        await message.answer(
            f'Please Enter your full name: eg: {html.italic("Abebe Kebede")}'
        )
    else:
        await state.update_data(name=user_input)
        await state.set_state(Form.phone_number)
        await message.answer(
            f"Great to meet you {html.quote(user_input)}! Please share your phone number with us.",
            reply_markup=ReplyKeyboardMarkup(
                keyboard=[
                    [
                        KeyboardButton(text="Share your Phone", request_contact=True),
                    ]
                ],
                resize_keyboard=True,
            ),
        )


@form_router.message(Form.phone_number)
async def process_phone_number(message: Message, state: FSMContext) -> None:
    print(message.contact)
    await state.update_data(phone_number=message.contact.phone_number)
    await state.set_state(Form.role)

    await message.answer(
        f"Your phone number is {message.contact.phone_number},",
        reply_markup=ReplyKeyboardMarkup(
            keyboard=[
                [
                    KeyboardButton(text="Driver"),
                    KeyboardButton(text="Passenger"),
                ]
            ]
        ),
    )


@form_router.message(Form.role)
async def process_role(message: Message, state: FSMContext) -> None:
    """The registration process is completed here. So this method saves the user into the database"""

    await state.update_data(role=message.text)
    data = await state.get_data()
    await message.answer(
        f"Registration Completed! {data}",
        reply_markup=ReplyKeyboardRemove(),
    )


async def main():
    global db_handler
    bot = Bot(token=BOT_TOKEN, parse_mode=ParseMode.HTML)
    dp = Dispatcher()
    dp.include_router(form_router)

    # try connecting to the database
    try:
        db_handler = DB_Handler()
    except Exception:
        return

    await dp.start_polling(bot)


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO, stream=sys.stdout)
    asyncio.run(main())
