from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import StatesGroup, State
from aiogram.types import Message, CallbackQuery
from aiogram.filters import Command, StateFilter
from telegram import bot, dp
from db import CodeModel
from ..cruds import (get_addresses,
                     get_unique_cities,
                     get_unique_places,
                     get_code_by_place_addr,
                     add_code_to_place)
from ..keyboards import create_inline_keyboard

class Form(StatesGroup):
    city = State()
    place_type = State()
    view_or_enter_code = State()
    address = State()
    enter_code = State()


@dp.message(lambda msg: msg.text.lower() == '🌆 выбрать город')
async def select_place(message: Message, state: FSMContext):
    cities = await get_unique_cities()

    kb = create_inline_keyboard(cities)

    await message.answer("Выберите город", reply_markup=kb)
    await state.set_state(Form.city)

@dp.message(Command('cancel'))
async def cancel(message: Message, state: FSMContext):
    await state.clear()
    await message.answer('Действие отменено')

@dp.callback_query(StateFilter(Form.city))
async def process_city(callback: CallbackQuery, state: FSMContext):
    await  state.update_data(city=callback.data)
    data = await state.get_data()
    city = data['city']

    places = await get_unique_places(city)
    kb = create_inline_keyboard(places)
    await callback.message.edit_text(text="Выберите тип", reply_markup=kb)
    await state.set_state(Form.place_type)

@dp.callback_query(StateFilter(Form.place_type))
async def process_place_type(callback: CallbackQuery, state: FSMContext):
    await state.update_data(place_type=callback.data)

    what_to_do = ["Найти код", "Ввести код"]
    kb = create_inline_keyboard(what_to_do)
    await callback.message.edit_text(text="Что хотите сделать?", reply_markup=kb)
    await state.set_state(Form.view_or_enter_code)

@dp.callback_query(StateFilter(Form.view_or_enter_code))
async def process_view_or_enter_code(callback: CallbackQuery, state: FSMContext):
    what_to_do = callback.data
    await state.update_data(what_to_do=what_to_do)
    data = await state.get_data()
    city = data['city']
    place_type = data['place_type']

    addresses = await get_addresses(place_type=place_type, city=city)
    kb = create_inline_keyboard(addresses)

    text = "По какому адресу хотите найти код?" if what_to_do == "Найти код" else "По какому адресу хотите добавить код?"
    await callback.message.edit_text(text=text, reply_markup=kb)
    await state.set_state(Form.address)

@dp.callback_query(StateFilter(Form.address))
async def process_address(callback: CallbackQuery, state: FSMContext):
    address = callback.data
    await state.update_data(address=address)
    data = await state.get_data()
    to_do = data["what_to_do"]

    if to_do == "Найти код":
        code = await get_code_by_place_addr(address=address)
        if code:
            await callback.message.edit_text(text=code.code)
            await state.clear()
            return

        await callback.message.edit_text(text="Ничего нет по этому адрессу ☹️")
        await state.clear()
        return

    await callback.message.edit_text(text="Отправь мне код сообщением")
    await state.set_state(Form.enter_code)

@dp.message(StateFilter(Form.enter_code))
async def enter_code(message: Message, state: FSMContext):
    data = await state.get_data()
    user_tg_id = str(message.from_user.id)
    code = message.text

    if not code.isdigit():
        await bot.send_message(chat_id=user_tg_id, text="Некорректный код. Отправь еще раз")
        return

    address = data['address']

    result = await add_code_to_place(address, user_tg_id, code)
    if isinstance(result, CodeModel):
        await bot.send_message(chat_id=user_tg_id, text="Успешно добавил")
        await state.clear()
        return
    await bot.send_message(chat_id=user_tg_id, text="Что-то пошло не так")
    await state.clear()





