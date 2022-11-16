from aiogram import types, Bot, Dispatcher
from config import *
import json
from requests import get
from asyncio import sleep
from aiogram.utils import executor

bot = Bot(token=5421418599:AAEhzHNgZVTlGp9LEWt6zOkAazBT9yiNGcg)
dp = Dispatcher(bot)


def send_price():
 """
 :get_sale:
 """
 result = get('https://api.ton.sh/getCoinPrice').text
 data = json.loads(result)
 price = data['result']

 return price

@dp.message_handler(text='/start')
async def get_price(m: types.Message):
 await m.reply(str(send_price()))

@dp.message_handler(text='bot.run_send_price()')
async def get_price1(m: types.Message):
 await m.reply('{"bot": "send_price"\n"ok": "True"}')
 while True:
  price = send_price()
  await bot.send_message(-1001545646667, f'Текущая цена TONcoin: {price}$')
  await sleep(60)

executor.start_polling(dp)
