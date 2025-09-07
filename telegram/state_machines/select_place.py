from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import StatesGroup, State
from aiogram.types import Message, CallbackQuery
from aiogram.filters import Command, StateFilter
from telegram import bot, dp
from ..cruds import get_places, get_unique_cities, get_unique_places
from ..keyboards import create_inline_keyboard

class Form(StatesGroup):
    city = State()
    place_type = State()
    code = State()


@dp.message(lambda msg: msg.text.lower() == 'найти код')
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
    await callback.message.edit_text(text="Выберите место", reply_markup=kb)
    await state.set_state(Form.place_type)

@dp.callback_query(StateFilter(Form.place_type))
async def process_place_type(callback: CallbackQuery, state: FSMContext):
    await state.update_data(place_type=callback.data)
    data = await state.get_data()

    places = await get_places(
        place_type=data['place_type'],
        city=data['city']
    )
    kb = create_inline_keyboard(places)
    await callback.message.edit_text(
        text="Выберите заведение",
        reply_markup=kb,
    )
    await state.set_state(Form.code)


