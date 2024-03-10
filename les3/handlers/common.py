from aiogram import types, F, Router
from aiogram.filters.command import Command
import logging
import random
from keyboards.keyboards import kb1, kb2
from utils.random_fox import fox
import requests  # Import requests library

router = Router()

# Function to get a random image URL
async def get_random_image(url):
    try:
        response = requests.get(url)
        response.raise_for_status()  # Raise error for non-200 status codes
        return response.json()['image']  # Assuming the JSON response contains a 'url' key
    except requests.exceptions.RequestException as e:
        logging.error(f"Error fetching random image: {e}")
        return None #data.get('image')#None

#Хэндлер на команду /start
@router.message(Command('start'))
async def cmd_start(message: types.Message):
    name = message.chat.first_name
    await message.answer(f'Привет, {name}', reply_markup=kb1)


#Хэндлер на команду /stop
@router.message(Command('stop'))
async def cmd_stop(message: types.Message):
    name = message.chat.first_name
    await message.answer(f'Пока, {name}')


#Хэндлер на команду /fox
@router.message(Command('fox'))
@router.message(Command('лиса'))
@router.message(F.text.lower() == 'покажи лису')
async def cmd_fox(message: types.Message):
    name = message.chat.first_name
    img_fox = fox()
    await message.answer(f'Держи лису, {name}')
    await message.answer_photo(photo=img_fox)
# await message.answer_
# await bot.send_photo(message.from_user.id, photo=img_fox)

# Хендлер на команду /random
@router.message(Command('random'))
async def cmd_random(message: types.Message):
    name = message.chat.first_name
    # Replace with your preferred random image API URL
    random_image_url = "https://randomfox.ca/floof/"  # Example using Picsum API
    img_url = await get_random_image(random_image_url)
    if img_url:
        await message.answer(f'Вот тебе случайная картинка, {name}')
        await message.answer_photo(photo=img_url)
    else:
        await message.answer(f'Не удалось найти картинку, попробуй позже.')


#Хендлер на сообщения
@router.message(F.text)
async def msg_echo(message: types.Message):
    msg_user = message.text.lower()
    name = message.chat.first_name
    if 'привет' in msg_user:
        await message.answer(f'Привет-привет, {name}')
    elif 'пока' == msg_user:
        await message.answer(f'Пока-пока, {name}')
    elif 'ты кто' in msg_user:
        await message.answer_dice(emoji="🎲")
    elif 'лиса' in msg_user:
        await message.answer(f'Смотри что у меня есть, {name}', reply_markup=kb2)
    else:
        await message.answer(f'Я не знаю такого слова')