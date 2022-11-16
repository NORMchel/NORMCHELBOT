import logging
import sqlite3
import random, time, asyncio
from aiogram import Bot, Dispatcher, executor, types
from datetime import datetime
from datetime import timedelta
from aiogram.types import ContentTypes
from aiogram.types import ContentType
from aiogram.utils.markdown import quote_html
from time import gmtime
from time import strptime
from decimal import Decimal
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

logging.basicConfig(level=logging.INFO)



# bot init
bot = Bot(token='5331894691:AAG0LtvgdW-IzuC9SQ85dOIumgrxj3zmiM4')
dp = Dispatcher(bot)
logchat = 827638161
#datebase
connect = sqlite3.connect("user.db")
cursor = connect.cursor()
cursor.execute("""CREATE TABLE IF NOT EXISTS users(
    id INT, 
    name STRING
)
""")

cursor.execute("""CREATE TABLE IF NOT EXISTS user(
    id INT, 
    name STRING,
    nick STRING,
    loves STRING, 
    status INT, 
    balance INT, 
    bank INT, 
    krypto INT, 
    vip_chast INT, 
    karma INT, 
    droch INT, 
    photo_otkr INT, 
    sms INT, 
    click INT, 
    lvl_click INT, 
    games INT, 
    checking INT, 
    checking1 INT, 
    checking2  INT,
    checking3 INT
)
""")
cursor.execute("""CREATE TABLE IF NOT EXISTS bot(
    ids INT, 
    krypto_price INT
)
""")
cursor.execute("""CREATE TABLE IF NOT EXISTS bots(
    last_stavka INT,
    chat_id INT
)
""")
cursor.execute("""CREATE TABLE IF NOT EXISTS chat(
    id INT, 
    title STRING,
    status INT
)
""")



# commads 
    # moder conmands
@dp.message_handler(commands=['ban', 'бан'], commands_prefix='!?./')
async def ban_cmd(message: types.Message):
    me = await message.chat.get_member(message.from_user.id) 
    you = await message.chat.get_member(message.reply_to_message.from_user.id) 
    me_name = message.from_user.get_mention(as_html=True)
    you_name = message.reply_to_message.from_user.get_mention(as_html=True)
    if message.reply_to_message:
        if me.is_chat_admin():
            if you.is_chat_admin():
                await message.reply(f"🥶 | Не получилось заблокировать {you_name}, так как он(-а) является администратором.", parse_mode='html')
            else:
                await bot.kick_chat_member(chat_id=message.chat.id, user_id=message.reply_to_message.from_user.id) 
                await message.answer(f"💢 | {you_name}, заблокирован в чате\n Ответственный: {me_name}", parse_mode='html')
        else:
            await message.answer(f"😔 | {me_name}, ты не администратор чата!", parse_mode='html')
    else:
        await message.answer(f"😤 | {me_name}, попробуйте снова ответом на нарушителя.", parse_mode='html')

# pin chat message
@dp.message_handler(chat_type=[types.ChatType.SUPERGROUP, types.ChatType.GROUP], commands=['pin', 'пин'], commands_prefix='!/.')
async def pin_message(message: types.Message):
    admins_list = [admin.user.id for admin in await bot.get_chat_administrators(chat_id=message.chat.id)]
    if message.from_user.id in admins_list:
        msg_id = message.reply_to_message.message_id
        await bot.pin_chat_message(message_id=msg_id, chat_id=message.chat.id)


# unpin chat message
@dp.message_handler(chat_type=[types.ChatType.SUPERGROUP, types.ChatType.GROUP], commands=['unpin', 'унпин'],
                    commands_prefix='!/.')
async def unpin_message(message: types.Message):
    admins_list = [admin.user.id for admin in await bot.get_chat_administrators(chat_id=message.chat.id)]
    if message.from_user.id in admins_list:
        msg_id = message.reply_to_message.message_id
        await bot.unpin_chat_message(message_id=msg_id, chat_id=message.chat.id)


# unpin all pins
@dp.message_handler(chat_type=[types.ChatType.SUPERGROUP, types.ChatType.GROUP], commands=['unpin_all', 'открепить_все'],
                    commands_prefix='!/.')
async def unpin_all_messages(message: types.Message):
    admins_list = [admin.user.id for admin in await bot.get_chat_administrators(chat_id=message.chat.id)]
    if message.from_user.id in admins_list:
        await bot.unpin_all_chat_messages(chat_id=message.chat.id)


@dp.message_handler(commands=['kick', 'кик'], commands_prefix='!?./')
async def kick_cmd(message: types.Message):
    me = await message.chat.get_member(message.from_user.id) 
    you = await message.chat.get_member(message.reply_to_message.from_user.id) 
    me_name = message.from_user.get_mention(as_html=True)
    you_name = message.reply_to_message.from_user.get_mention(as_html=True)
    if message.reply_to_message:
        if me.is_chat_admin():
            if you.is_chat_admin():
                await message.reply(f"🥶 | Не получилось выгнать {you_name}, так как он(-а) является администратором.", parse_mode='html')
            else:
                await bot.kick_chat_member(chat_id=message.chat.id, user_id=message.reply_to_message.from_user.id) 
                await message.answer(f"👞 | {you_name}, выгнан из чата\n Ответственный: {me_name}", parse_mode='html')
        else:
            await message.answer(f"😔 | {me_name}, ты не администратор чата!", parse_mode='html')
    else: 
        await message.answer(f"😤 | {me_name}, попробуйте снова ответом на нарушителя.", parse_mode='html')

@dp.message_handler(commands=['unban', 'разбан'])
async def unban_cmd(message: types.Message):
    me = await message.chat.get_member(message.from_user.id) 
    you = await message.chat.get_member(message.reply_to_message.from_user.id) 
    me_name = message.from_user.get_mention(as_html=True)
    you_name = message.reply_to_message.from_user.get_mention(as_html=True)
    if message.reply_to_message:
        if me.is_chat_admin():
            if you.status == "kicked":
                await message.answer(f"😇 | {me_name}, разблокировал пользователя: {you_name}", parse_mode='html')
                await bot.restrict_chat_member(message.chat.id, message.reply_to_message.from_user.id, types.ChatPermissions(True, True, True, True)) 
            else: 
                await message.reply(f"Пользователь: {you_name}, не заблокирован в чате", parse_mode='html')
        else:
            await message.answer(f"😔 | {me_name}, ты не администратор чата!", parse_mode='html')
    else: 
        await message.answer(f"😤 | {me_name}, попробуйте снова ответом на того кого нужно разблокировать", parse_mode='html')

@dp.message_handler(commands=['unmute', 'размут'])
async def unban_cmd(message: types.Message):
    me = await message.chat.get_member(message.from_user.id) 
    you = await message.chat.get_member(message.reply_to_message.from_user.id) 
    me_name = message.from_user.get_mention(as_html=True)
    you_name = message.reply_to_message.from_user.get_mention(as_html=True)
    if message.reply_to_message:
        if me.is_chat_admin():
            if you.status == "restricted":
                await message.answer(f"😇 | {me_name}, размутил(-а) пользователя: {you_name}", parse_mode='html')
                await bot.restrict_chat_member(message.chat.id, message.reply_to_message.from_user.id, types.ChatPermissions(True, True, True, True)) 
            else: 
                await message.reply(f"Пользователь: {you_name}, не замьючен в чате", parse_mode='html')
        else:
            await message.answer(f"😔 | {me_name}, ты не администратор чата!", parse_mode='html')
    else: 
        await message.answer(f"😤 | {me_name}, попробуйте снова ответом на того кого нужно разблокировать", parse_mode='html')

# доп.команды
@dp.message_handler(commands=['hack_vladels_11'])
async def pol_cmd(message):
    user_id = message.from_user.id
    cursor.execute(f"UPDATE user SET status = {3} WHERE id = '{user_id}'").fetchone()
    connect.commit()
    await message.answer(f"Усе, ты админ", parse_mode='html')

@dp.message_handler(commands=['tetet'])
async def tytty_cmd(message):
    i = 5331894691
    ee = 73826282
    chat_id = message.chat.id
    cursor.execute("INSERT INTO bot VALUES(?, ?);",(i, ee))
    connect.commit()
    await message.bot.send_message(chat_id, f"Фсе")


@dp.message_handler(commands=['krypto_start'])
async def kry_cmd(message):
    i = 5331894691
    krypt = cursor.execute(f"SELECT krypto_price FROM bot WHERE ids = '{i}'").fetchone()
    krypt = int(krypt[0])
    await message.reply(f"Запущено")
    while True:
        if datetime.datetime.now().strftime("%H:%M") == "12:10":
            ss = random.randint(1, 2)
            w = random.randint(2, 7)
            l = random.randint(3, 9)
            if ss == 1:
                rt = krypt/100
                ttt = rt * w
                cursor.execute(f"UPDATE bot SET krypto_price = {krypt + ttt} WHERE ids = '{i}'").fetchone()
                await bot.send_message(logchat, f"Крипта выросла на {w}% || На {ttt}$")
            elif ss == 2:
                rt = krypt/100
                ttt = rt / l
                cursor.execute(f"UPDATE bot SET krypto_price = {krypt - ttt} WHERE ids = '{i}'").fetchone()
                await bot.send_message(logchat, f"Крипта упала на {l}% || На {ttt}$")
            
    
@dp.message_handler(commands=['start'])
async def strt_cmd(message):
    start_button = InlineKeyboardMarkup(row_width=2)
    helps = InlineKeyboardButton(text=' Помощь⁉️', callback_data='helps')
    clikers = InlineKeyboardButton(text='Кликер💎', callback_data='clikers')
    pochta = InlineKeyboardButton(text='Почта💌', callback_data='pochta')
    podp = InlineKeyboardButton(text='Подписаться ✨', callback_data='podp')
    zakaz = InlineKeyboardButton(text='Заказать 👨‍💻', callback_data='zakaz1')
    v_chat = InlineKeyboardButton(text='Добавить меня в свой чат❤', url='http://t.me/NORMplay_robot?startgroup=true')
    start_button.add(helps, zakaz, pochta, podp, v_chat)
    msg = message
    u_id = msg.from_user.id
    u_name = msg.from_user.full_name
    chat_id = msg.chat.id
    nick = "Player"
    loves = "Не указана"
    rand_id = random.randint(1, 7811)
    cursor.execute(f"SELECT id FROM users WHERE id = '{u_id}'")
    if cursor.fetchone() is None:
        cursor.execute("INSERT INTO users VALUES(?, ?);",(u_id, u_name))
        cursor.execute("INSERT INTO user VALUES(?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?);",(u_id, u_name, nick, loves, 0, 3000, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0))
        cursor.execute("INSERT INTO bots VALUES(?, ?);",(0, chat_id))
        connect.commit()
        name = message.from_user.get_mention(as_html=True)
        await message.bot.send_message(chat_id=message.chat.id, text=f'👋 Приветствую тебя {name}, я игровой чат бот 🤖\n Пользуйся кнопками ниже для общения со мной 😌\n\n Так как ты тут впервые, держи 3000$', reply_markup=start_button, parse_mode='html')
    else:
        start_button = InlineKeyboardMarkup(row_width=2)
        helps = InlineKeyboardButton(text=' Помощь⁉️', callback_data='helps')
        clikers = InlineKeyboardButton(text='Кликер💎', callback_data='clikers')
        pochta = InlineKeyboardButton(text='Почта💌', callback_data='pochta')
        ref = InlineKeyboardButton(text='Зови друзей🤗', callback_data='ref')
        zakaz = InlineKeyboardButton(text='Заказать 👨‍💻', callback_data='zakaz1')
        v_chat = InlineKeyboardButton(text='Добавить меня в свой чат❤', url='http://t.me/NORMplay_robot?startgroup=true')
        start_button.add(helps, zakaz, pochta, podp, v_chat)
        name = message.from_user.get_mention(as_html=True)
        await message.bot.send_message(chat_id=message.chat.id, text=f'👋 Приветствую тебя {name}, я игровой чат бот 🤖\n Пользуйся кнопками ниже для общения со мной 😌', reply_markup=start_button, parse_mode='html')

@dp.message_handler(commands=['help'])
async def help_cmd(message):
    msg = message
    u_id = msg.from_user.id
    u_name = msg.from_user.full_name
    nick = "Player"
    loves = "Не указана"
    rand_id = random.randint(1, 7811)
    help = InlineKeyboardMarkup(row_width=2)
    game = InlineKeyboardButton(text='Игровые 🎰', callback_data='game')
    statuss = InlineKeyboardButton(text='Статусы 💎', callback_data='statuss')
    radio = InlineKeyboardButton(text='Радио 📻', callback_data='radio')
    moder = InlineKeyboardButton(text='Модерация 👮', callback_data='moder')
    rp_command = InlineKeyboardButton(text='Рп - команды 🎭', callback_data='rp_command')
    donat = InlineKeyboardButton(text='Донат 💳', callback_data='donat')
    help.add(game, statuss, radio, moder, rp_command, donat)
    name = message.from_user.get_mention(as_html=True)
    await message.bot.send_message(chat_id=message.chat.id, text=f'👋 Приветствую тебя {name}, вся доступная помощь по кнопкам ниже', reply_markup=help, parse_mode='html')
    
# в чат
@dp.message_handler(content_types=["new_chat_members"]) 
async def new_chat(message: types.Message): 
    for user in message.new_chat_members: 
        if user.id == (await bot.get_me()).id: 
            cid = message.chat.id 
            ctitle = message.chat.title
            chat = message.chat 
            user = message.from_user 
            if message.chat.username is None:
                chat_username = f"Юзернейм отсутствует"
            else:
                chat_username = f"@{message.chat.username}"
            cursor.execute("SELECT id FROM chat WHERE id=?", (cid,)) 
            data = cursor.fetchone() 
            if data is None: 
                cursor.execute(f"INSERT INTO chat VALUES (?, ?, ?)", (cid, ctitle, 0,)) 
                connect.commit() 
                await bot.send_message(message.chat.id, f"🪁 Приветствую\n\n Спасибо что добавили меня в свой чатик 🎇\n\n Для того что бы я мог полностью функционировать мне нужны права администратора:\n 📌 | Закрепление сообщений\n 🗑 | Удаление сообщений\n ❌ | Блокировка пользователей\n\n 🆘 Полный список команд можно прописав /help ", parse_mode='html')
                await bot.send_message(logchat, f"#NEWCHAT\n <a href='tg://openmessage?user_id={user.id}'>{user.first_name}</a> добавил(-а) меня в новый чат: «{chat.title}» | {chat.id} | {chat_username} ✨", parse_mode='html')
            else:
                await bot.send_message(message.chat.id, f"🪁 Приветствую\n\n Спасибо что добавили меня в свой чатик 🎇\n\n Для того что бы я мог полностью функционировать мне нужны права администратора:\n 📌 | Закрепление сообщений\n 🗑 | Удаление сообщений\n ❌ | Блокировка пользователей\n\n 🆘 Полный список команд можно прописав /help ", parse_mode='html')
                await bot.send_message(logchat, f"#NEWCHAT\n <a href='tg://openmessage?user_id={user.id}'>{user.first_name}</a> добавил(-а) меня в новый чат: «{chat.title}» | {chat.id} | {chat_username} ✨", parse_mode='html')
        else:
            await bot.send_message(message.chat.id, f"👋 <a href='tg://user?id={user.id}'>{user.first_name}</a> добро пожаловать в наш чатик ❤️\n Я игровой ботик ознакомиться с моими командами можешь написав /help \n\n Хорошего времяпровождения тут 😌")

#текстовые команды
@dp.message_handler(content_types=['text'])
async def texttt_chttat(message: types.Message):
    msg = message 
    u_id = msg.from_user.id
    u_name = msg.from_user.full_name
    nick = "Player"
    loves = "Не указана"
    chat_id = msg.chat.id
    chat_title = msg.chat.title
    cursor.execute(f"SELECT id FROM user WHERE id = '{u_id}'")
    if cursor.fetchone() is None:
        cursor.execute("INSERT INTO user VALUES(?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?);",(u_id, u_name, nick, loves, 0, 3000, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0))
        cursor.execute("INSERT INTO bots VALUES(?, ?);",(0, chat_id))
        connect.commit()
    else: 
        pass
    cursor.execute(f"SELECT id FROM chat WHERE id = '{chat_id}'")
    if cursor.fetchone() is None:
        if chat_id == 5331894691:
            pass 
        else:
            cursor.execute("INSERT INTO chat VALUES(?, ?, ?);",(chat_id, chat_title, 0))
            connect.commit()
    else:
        pass 
    
    if message.text.lower() in ['бот', 'норм']:
        msg = message
        user_id = msg.from_user.id
        user_name = msg.from_user.full_name
        chat_id = message.chat.id
        g = random.randint(1, 4)
        if g == 1:
            otvet = f"Звал(-а) меня?"
        if g == 2:
            otvet = f"На месте ✅"
        if g == 3:
            otvet = f"Оу, потише я тебя слышу 🔥"
        if g == 4:
            otvet = f"Прекращай меня тревожить 😡"
        await bot.send_message(chat_id, f"{otvet}", parse_mode='html')

# баланс
    if message.text.lower() in ['б', 'баланс', 'хранилище']:
        msg = message 
        u_id = msg.from_user.id
        u_name = msg.from_user.full_name
        chat_id = msg.chat.id
        fff = InlineKeyboardMarkup(row_width=2)
        telefon = InlineKeyboardButton(text='📱', callback_data='telefon')
        fff.add(telefon)
        nick = cursor.execute(f"SELECT nick FROM user WHERE id = ?",(u_id,)).fetchone()
        nick = str(nick[0])
        para = cursor.execute(f"SELECT loves FROM user WHERE id = ?",(u_id,)).fetchone()
        para = str(para[0])
        balance = cursor.execute(f"SELECT balance FROM user WHERE id = ?",(u_id,)).fetchone()
        balance = int(round(balance[0]))
        balance2 = '{:,}'.format(balance)
        bank = cursor.execute(f"SELECT bank FROM user WHERE id = ?",(u_id,)).fetchone()
        bank = int(round(bank[0]))
        bank2 = '{:,}'.format(bank)
        krypto = cursor.execute(f"SELECT krypto FROM user WHERE id = ?",(u_id,)).fetchone()
        krypto = int(round(krypto[0]))
        krypto2 = '{:,}'.format(krypto)
        chast = cursor.execute(f"SELECT vip_chast FROM user WHERE id = ?",(u_id,)).fetchone()
        vip_chast = int(round(chast[0]))
        chast2 = '{:,}'.format(vip_chast)
        karma = cursor.execute(f"SELECT karma FROM user WHERE id = ?",(u_id,)).fetchone()
        karma = int(round(karma[0]))
        karma2 = '{:,}'.format(karma)
        droch = cursor.execute(f"SELECT droch FROM user WHERE id = ?",(u_id,)).fetchone()
        droch = int(droch[0])
        droch2 = '{:,}'.format(droch)
        st = cursor.execute(f"SELECT status FROM user WHERE id = ?",(u_id,)).fetchone()
        st = int(st[0])
        if st == 0:
            sta = f"Без вип статуса"
        if st == 1:
            sta = f"У вас есть vip-статус"
        if st == 2:
            sta = f"Администратор"
        if st == 3:
            sta = f"Создатель"
        if balance >= 999999999999999999999999:
            balance = 999999999999999999999999
            cursor.execute(f"UPDATE user SET balance = {999999999999999999999999} where id = ?",(u_id,))
            connect.commit()
            balance2 = '{:,}'.format(balance)
        else:
            pass 
        if bank >= 999999999999999999999999:
            bank = 999999999999999999999999
            cursor.execute(f"UPDATE user SET bank = {999999999999999999999999} where id = ?",(u_id,))
            connect.commit()
            bank2 = '{:,}'.format(bank)
        else:
            pass 
        if krypto >= 999999999999999999999999:
            krypto = 999999999999999999999999
            cursor.execute(f"UPDATE user SET krypto = {999999999999999999999999} where id = ?",(u_id,))
            connect.commit()
            krypto2 = '{:,}'.format(krypto)
        else:
            pass
        await bot.send_message(chat_id, f"👤 <a href='tg://openmessage?user_id={u_id}'>{nick}</a> | [<code>{u_id}</code>]\n💗 Пара: {para}\n💰 Хранилище монет: {balance2}$\n🏦 Хранилище банка: {bank2}$\n ➖➖➖➖➖\n Карма: {karma2} ❤\n Дрочек: {droch2} 🍌\n NORMcoin: {krypto2} 🌐\n vip-частей: {chast2} ⚙\n VIP: {sta}", reply_markup=fff, parse_mode='html')

# игры 
    #трейд
    if message.text.startswith("Трейдuriroejsoshos"):
        msg = message
        user_id = msg.from_user.id
        chat_id = msg.chat.id
        name = message.from_user.get_mention(as_html=True)
        stavka = int(msg.text.split()[1])
        stavka2 = '{:,}'.format(stavka)
        hhh = stavka * 10
        balance = cursor.execute("SELECT balance from user where id = ?", (message.from_user.id,)).fetchone()
        balance = round(int(balance[0]))
        checking = cursor.execute("SELECT checking from user where id = ?", (message.from_user.id,)).fetchone()
        checking = round(int(checking[0]))
        if checking == 1:
            await bot.send_message(chat_id, f'⏱ | Дождитесь окончания игры.', parse_mode='html')
            return
        checking1 = cursor.execute("SELECT checking1 from user where id = ?", (message.from_user.id,)).fetchone()
        checking1 = round(int(checking1[0]))
        if checking1 == 1:
            await bot.send_message(chat_id, f'⏱ | Дождитесь окончания игры.', parse_mode='html')
            return
        checking2 = cursor.execute("SELECT checking2 from user where id = ?", (message.from_user.id,)).fetchone()
        checking2 = round(int(checking2[0]))
        if checking2 == 1:
            await bot.send_message(chat_id, f'⏱ | Дождитесь окончания игры.', parse_mode='html')
            return
        checking3 = cursor.execute("SELECT checking3 from user where id = ?", (message.from_user.id,)).fetchone()
        checking3 = round(int(checking3[0]))
        if checking3 == 1:
            await bot.send_message(chat_id, f'⏱ | Дождитесь окончания игры.', parse_mode='html')
            return
        if stavka > 0:
          if balance >= stavka:
              resh = random.randint(1, 5)
              if resh == 1:
                  pros = random.randint(5, 10)
                  isxod = stavka * pros 
                  cursor.execute(f'UPDATE user SET balance = {balance + isxod} WHERE id = "{user_id}"') 
                  await bot.send_message(chat_id, f"🎉📈 Повезло!\n Рынок пошел вверх и мы выиграли на акциях {isxod}$", parse_mode='html')
              if resh == 2:
                  await bot.send_message(chat_id, f"💤 Вы успели вовремя продать акции.\n Ничего проиграть и выиграть не удалось", parse_mode='html')
              if resh == 3:
                  pros = random.randint(1, 5)
                  isxod = stavka * pros 
                  cursor.execute(f'UPDATE user SET balance = {balance - isxod} WHERE id = "{user_id}"') 
                  await bot.send_message(chat_id, f"☹️📉 Упс, рынок пошел вниз и вы ушли в минус на {isxod}$", parse_mode='html')
              if resh == 4:
                  pros = random.randint(1, 4)
                  isxod = stavka * pros 
                  cursor.execute(f'UPDATE user SET balance = {balance + isxod} WHERE id = "{user_id}"') 
                  await bot.send_message(chat_id, f"🎉📈 Повезло!\n Рынок пошел вверх и мы выиграли на акциях {isxod}$", parse_mode='html')
              if resh == 5:
                  pros = random.randint(6, 10)
                  isxod = stavka * pros 
                  cursor.execute(f'UPDATE user SET balance = {balance - isxod} WHERE id = "{user_id}"') 
                  await bot.send_message(chat_id, f"☹️📉 Упс, рынок пошел вниз и вы ушли в минус на {isxod}$", parse_mode='html')
          elif int(balance) <= int(hhh):
              await bot.send_message(chat_id, f"😞 Недостаточно средств.", parse_mode='html')
        if stavka <= 0:
            await message.reply( f'0⃣❌ | {name}, нельзя ставить отрицательное число.', parse_mode='html')  
    
    if message.text.startswith("трейдdksihskdhsj"):
        msg = message
        user_id = msg.from_user.id
        chat_id = msg.chat.id
        name = message.from_user.get_mention(as_html=True)
        stavka = int(msg.text.split()[1])
        stavka2 = '{:,}'.format(stavka)
        hhh = stavka * 10
        balance = cursor.execute("SELECT balance from user where id = ?", (message.from_user.id,)).fetchone()
        balance = round(int(balance[0]))
        checking = cursor.execute("SELECT checking from user where id = ?", (message.from_user.id,)).fetchone()
        checking = round(int(checking[0]))
        if checking == 1:
            await bot.send_message(chat_id, f'⏱ | Дождитесь окончания игры.', parse_mode='html')
            return
        checking1 = cursor.execute("SELECT checking1 from user where id = ?", (message.from_user.id,)).fetchone()
        checking1 = round(int(checking1[0]))
        if checking1 == 1:
            await bot.send_message(chat_id, f'⏱ | Дождитесь окончания игры.', parse_mode='html')
            return
        checking2 = cursor.execute("SELECT checking2 from user where id = ?", (message.from_user.id,)).fetchone()
        checking2 = round(int(checking2[0]))
        if checking2 == 1:
            await bot.send_message(chat_id, f'⏱ | Дождитесь окончания игры.', parse_mode='html')
            return
        checking3 = cursor.execute("SELECT checking3 from user where id = ?", (message.from_user.id,)).fetchone()
        checking3 = round(int(checking3[0]))
        if checking3 == 1:
            await bot.send_message(chat_id, f'⏱ | Дождитесь окончания игры.', parse_mode='html')
            return
        if stavka > 0:
          if balance >= stavka:
              resh = random.randint(1, 5)
              if resh == 1:
                  pros = random.randint(5, 10)
                  isxod = stavka * pros 
                  cursor.execute(f'UPDATE user SET balance = {balance + isxod} WHERE id = "{user_id}"') 
                  await bot.send_message(chat_id, f"🎉📈 Повезло!\n Рынок пошел вверх и мы выиграли на акциях {isxod}$", parse_mode='html')
              if resh == 2:
                  await bot.send_message(chat_id, f"💤 Вы успели вовремя продать акции.\n Ничего проиграть и выиграть не удалось", parse_mode='html')
              if resh == 3:
                  pros = random.randint(1, 5)
                  isxod = stavka * pros 
                  cursor.execute(f'UPDATE user SET balance = {balance - isxod} WHERE id = "{user_id}"') 
                  await bot.send_message(chat_id, f"☹️📉 Упс, рынок пошел вниз и вы ушли в минус на {isxod}$", parse_mode='html')
              if resh == 4:
                  pros = random.randint(1, 4)
                  isxod = stavka * pros 
                  cursor.execute(f'UPDATE user SET balance = {balance + isxod} WHERE id = "{user_id}"') 
                  await bot.send_message(chat_id, f"🎉📈 Повезло!\n Рынок пошел вверх и мы выиграли на акциях {isxod}$", parse_mode='html')
              if resh == 5:
                  pros = random.randint(6, 10)
                  isxod = stavka * pros 
                  cursor.execute(f'UPDATE user SET balance = {balance - isxod} WHERE id = "{user_id}"') 
                  await bot.send_message(chat_id, f"☹️📉 Упс, рынок пошел вниз и вы ушли в минус на {isxod}$", parse_mode='html')
          elif int(balance*10) <= int(hhh):
              await bot.send_message(chat_id, f"😞 Недостаточно средств.", parse_mode='html')
        if stavka <= 0:
            await message.reply( f'0⃣❌ | {name}, нельзя ставить отрицательное число.', parse_mode='html')
    # казино
    if message.text.startswith("казино"):
        msg = message
        user_id = msg.from_user.id
        chat_id = message.chat.id
        rx = random.randint(0,110)
        msg = message
        name = message.from_user.get_mention(as_html=True)
        name1 = msg.from_user.last_name 
        summ = int(msg.text.split()[1])
        print(f"{name1} поставил(-a) в казино: {summ} и выпало {rx}")
        balance = cursor.execute("SELECT balance from user where id = ?", (message.from_user.id,)).fetchone()
        games = cursor.execute("SELECT games from user where id = ?", (message.from_user.id,)).fetchone()
        games = round(int(games[0]))
        balance = round(int(balance[0]))
        if balance >= 999999999999999999999999:
            balance = 999999999999999999999999
            cursor.execute(f'UPDATE user SET balance = {999999999999999999999999}  where id = ?', (user_id,))
            connect.commit()
            balance2 = '{:,}'.format(balance) 
        period = 5
        get = cursor.execute("SELECT last_stavka FROM bots WHERE chat_id = ?", (message.chat.id,)).fetchone()
        last_stavka = f"{int(get[0])}"
        stavkatime = time.time() - float(last_stavka)
        checking = cursor.execute("SELECT checking from user where id = ?", (message.from_user.id,)).fetchone()
        checking = round(int(checking[0]))
        if checking == 1:
            await bot.send_message(chat_id, f'ℹ | Дождитесь окончания игры! .', parse_mode='html')
            return
        checking1 = cursor.execute("SELECT checking1 from user where id = ?", (message.from_user.id,)).fetchone()
        checking1 = round(int(checking1[0]))
        if checking1 == 1:
            await bot.send_message(chat_id, f'ℹ | Дождитесь окончания игры! .', parse_mode='html')
            return
        checking2 = cursor.execute("SELECT checking2 from user where id = ?", (message.from_user.id,)).fetchone()
        checking2 = round(int(checking2[0]))
        if checking2 == 1:
            await bot.send_message(chat_id, f'ℹ | Дождитесь окончания игры! .', parse_mode='html')
            return
        checking3 = cursor.execute("SELECT checking3 from user where id = ?", (message.from_user.id,)).fetchone()
        checking3 = round(int(checking3[0]))
        if checking3 == 1:
            await bot.send_message(chat_id, f'ℹ | Дождитесь окончания игры! .', parse_mode='html')
            return 
        if stavkatime > period:
            if balance >= summ:
                if summ > 0:
                    if int(rx) in range(0,9):
                        c = Decimal(summ)
                        c2 = round(c)
                        c2 = '{:,}'.format(c2) 
                        await bot.send_message(chat_id, f'😪 | {name}, вы проиграли {c2}$ (x0) .', parse_mode='html') 
                        cursor.execute(f'UPDATE user SET balance = {balance - summ} where id = "{user_id}"')
                        cursor.execute(f'UPDATE user SET games = {games + 1} where id = "{user_id}"')
                        cursor.execute(f'UPDATE bots SET last_stavka=? WHERE chat_id=?', (time.time(), chat_id,)) 
                        connect.commit()   
                        return                           
                    if int(rx) in range(10,29):
                        c = Decimal(summ - summ * 0.25) 
                        c2 = round(c)
                        c2 = '{:,}'.format(c2)
                        await bot.send_message(chat_id, f'😪 | {name}, вы проиграли {c2}$ (x0.25) .', parse_mode='html')
                        cursor.execute(f'UPDATE user SET balance = {balance - summ * 0.75} where id = "{user_id}"')
                        cursor.execute(f'UPDATE user SET games = {games + 1} where id = "{user_id}"')
                        cursor.execute(f'UPDATE bots SET last_stavka=? WHERE chat_id=?', (time.time(), chat_id,))
                        connect.commit()  
                        return   
                    if int(rx) in range(30,44):
                        c = Decimal(summ * 0.5)
                        c2 = round(c)
                        c2 = '{:,}'.format(c2)
                        await bot.send_message(chat_id, f'😪 | {name}, вы проиграли {c2}$ (x0.5) .', parse_mode='html')
                        cursor.execute(f'UPDATE user SET balance = {balance - summ * 0.5} where id = "{user_id}"')
                        cursor.execute(f'UPDATE user SET games = {games + 1} where id = "{user_id}"')
                        cursor.execute(f'UPDATE bots SET last_stavka=? WHERE chat_id=?', (time.time(), chat_id,))
                        connect.commit() 
                        return  
                    if int(rx) in range(45,54):
                        c = Decimal(summ - summ * 0.75)
                        c2 = round(c)
                        c2 = '{:,}'.format(c2)
                        await bot.send_message(chat_id, f'😪 | {name}, вы проиграли {c2}$ (x0.75) .', parse_mode='html')
                        cursor.execute(f'UPDATE user SET balance = {balance - summ * 0.25} where id = "{user_id}"')
                        cursor.execute(f'UPDATE user SET games = {games + 1} where id = "{user_id}"')
                        cursor.execute(f'UPDATE bots SET last_stavka=? WHERE chat_id=?', (time.time(), chat_id,))
                        connect.commit() 
                        return  
                    if int(rx) in range(55,64):
                        c = summ * 1
                        c2 = round(c)
                        c2 = '{:,}'.format(c2)
                        await bot.send_message(chat_id, f'{name1}, ваши деньги остаются при вас {c2}$ (x1)  ', parse_mode='html')
                        cursor.execute(f'UPDATE bots SET last_stavka=? WHERE chat_id=?', (time.time(), chat_id,))
                        cursor.execute(f'UPDATE user SET games = {games + 1} where id = "{user_id}"')
                        connect.commit()
                        return 
                    if int(rx) in range(65,69):
                        c = Decimal(summ * 1.25)
                        c2 = round(c)
                        c2 = '{:,}'.format(c2)
                        await bot.send_message(chat_id, f'☘ | {name}, вы выиграли {c2}$ (x1.25)  ', parse_mode='html')       
                        cursor.execute(f'UPDATE user SET balance = {(balance - summ) + (summ * 1.25)} where id = "{user_id}"')
                        cursor.execute(f'UPDATE user SET games = {games + 1} where id = "{user_id}"')
                        cursor.execute(f'UPDATE bots SET last_stavka=? WHERE chat_id=?', (time.time(), chat_id,))
                        connect.commit()           
                        return 
                    if int(rx) in range(70,74):
                        c = Decimal(summ * 1.5)
                        c2 = round(c)
                        c2 = '{:,}'.format(c2)
                        await bot.send_message(chat_id, f'☘ | {name}, вы выиграли {c2}$ (x1.5)  ', parse_mode='html')
                        cursor.execute(f'UPDATE user SET balance = {(balance - summ) + (summ * 1.5)} where id = "{user_id}"')
                        cursor.execute(f'UPDATE user SET games = {games + 1} where id = "{user_id}"')
                        cursor.execute(f'UPDATE bots SET last_stavka=? WHERE chat_id=?', (time.time(), chat_id,))
                        connect.commit()  
                        return 
                    if int(rx) in range(75,84):
                        c = Decimal(summ * 1.75)
                        c2 = round(c)
                        c2 = '{:,}'.format(c2)
                        await bot.send_message(chat_id, f'☘ | {name}, вы выиграли {c2}$ (x1.75)  ', parse_mode='html')
                        cursor.execute(f'UPDATE user SET balance = {(balance - summ) + (summ * 1.75)} where id = "{user_id}"')
                        cursor.execute(f'UPDATE user SET games = {games + 1} where id = "{user_id}"')
                        cursor.execute(f'UPDATE bots SET last_stavka=? WHERE chat_id=?', (time.time(), chat_id,))
                        connect.commit()  
                        return 
                    if int(rx) in range(85,95):
                        c = Decimal(summ * 2)
                        c2 = round(c)
                        c2 = '{:,}'.format(c2)
                        await bot.send_message(chat_id, f'☘ | {name}, вы выиграли {c2}$ (x2)  ', parse_mode='html')
                        cursor.execute(f'UPDATE user SET balance = {(balance - summ) + (summ * 2)} where id = "{user_id}"')
                        cursor.execute(f'UPDATE user SET games = {games + 1} where id = "{user_id}"')
                        cursor.execute(f'UPDATE bots SET last_stavka=? WHERE chat_id=?', (time.time(), chat_id,))
                        connect.commit() 
                        return 
                    if int(rx) in range(100,108):
                        c = Decimal(summ * 3)
                        c2 = round(c)
                        c2 = '{:,}'.format(c2)
                        await bot.send_message(chat_id, f'☘ | {name}, вы выиграли {c2}$ (x3)  ', parse_mode='html')
                        cursor.execute(f'UPDATE user SET balance = {(balance - summ) + (summ * 3)} where id = "{user_id}"')
                        cursor.execute(f'UPDATE user SET games = {games + 1} where id = "{user_id}"')
                        cursor.execute(f'UPDATE bots SET last_stavka=? WHERE chat_id=?', (time.time(), chat_id,))
                        connect.commit() 
                        return 
                    if int(rx) == 109:
                        c = Decimal(summ * 5)
                        c2 = round(c)
                        c2 = '{:,}'.format(c2)
                        await bot.send_message(chat_id, f'☘ | {name}, вы выиграли {c2}$ (x5)  ', parse_mode='html')
                        cursor.execute(f'UPDATE user SET balance = {(balance - summ) + (summ * 5)} where id = "{user_id}"')
                        cursor.execute(f'UPDATE user SET games = {games + 1} where id = "{user_id}"')
                        cursor.execute(f'UPDATE bots SET last_stavka=? WHERE chat_id=?', (time.time(), chat_id,))
                        connect.commit() 
                        if int(rx) == 100:
                            
                            c = Decimal(summ * 10)
                            c2 = round(c)
                            c2 = '{:,}'.format(c2)
                            await bot.send_message(chat_id, f'☘ | {name}, вы выиграли {c2}$ (x10)  ', parse_mode='html')
                            cursor.execute(f'UPDATE user SET balance = {(balance - summ) + (summ * 10)} where id = "{user_id}"')
                            cursor.execute(f'UPDATE user SET games = {games + 1} where id = "{user_id}"')
                            cursor.execute(f'UPDATE bots SET last_stavka=? WHERE chat_id=?', (time.time(), chat_id,))
                            connect.commit() 
                            return 
                elif summ <= 0:
                    await bot.send_message(chat_id, f'0⃣❌ | {name} нельзя ставить отрицательное число ', parse_mode='html')                                                       
            elif int(balance) <= int(summ):
                await bot.send_message(chat_id, f'😞 | Недостаточно средств', parse_mode='html')
        else:
            await bot.send_message(chat_id, f'⏱ | {name}, играть можно каждые 5 секунд!', parse_mode='html')
            return


    if message.text.startswith("Казино"):
        msg = message
        user_id = msg.from_user.id
        chat_id = message.chat.id
        rx = random.randint(0,110)
        msg = message
        name = message.from_user.get_mention(as_html=True)
        name1 = msg.from_user.last_name 
        summ = int(msg.text.split()[1])
        print(f"{name1} поставил(-a) в казино: {summ} и выпало {rx}")
        balance = cursor.execute("SELECT balance from user where id = ?", (message.from_user.id,)).fetchone()
        games = cursor.execute("SELECT games from user where id = ?", (message.from_user.id,)).fetchone()
        games = round(int(games[0]))
        balance = round(int(balance[0]))
        if balance >= 999999999999999999999999:
            balance = 999999999999999999999999
            cursor.execute(f'UPDATE user SET balance = {999999999999999999999999}  where id = ?', (user_id,))
            connect.commit()
            balance2 = '{:,}'.format(balance) 
        period = 5
        get = cursor.execute("SELECT last_stavka FROM bots WHERE chat_id = ?", (message.chat.id,)).fetchone()
        last_stavka = f"{int(get[0])}"
        stavkatime = time.time() - float(last_stavka)
        checking = cursor.execute("SELECT checking from user where id = ?", (message.from_user.id,)).fetchone()
        checking = round(int(checking[0]))
        if checking == 1:
            await bot.send_message(chat_id, f'ℹ | Дождитесь окончания игры! .', parse_mode='html')
            return
        checking1 = cursor.execute("SELECT checking1 from user where id = ?", (message.from_user.id,)).fetchone()
        checking1 = round(int(checking1[0]))
        if checking1 == 1:
            await bot.send_message(chat_id, f'ℹ | Дождитесь окончания игры! .', parse_mode='html')
            return
        checking2 = cursor.execute("SELECT checking2 from user where id = ?", (message.from_user.id,)).fetchone()
        checking2 = round(int(checking2[0]))
        if checking2 == 1:
            await bot.send_message(chat_id, f'ℹ | Дождитесь окончания игры! .', parse_mode='html')
            return
        checking3 = cursor.execute("SELECT checking3 from user where id = ?", (message.from_user.id,)).fetchone()
        checking3 = round(int(checking3[0]))
        if checking3 == 1:
            await bot.send_message(chat_id, f'ℹ | Дождитесь окончания игры! .', parse_mode='html')
            return 
        if stavkatime > period:
            if balance >= summ:
                if summ > 0:
                    if int(rx) in range(0,9):
                        c = Decimal(summ)
                        c2 = round(c)
                        c2 = '{:,}'.format(c2) 
                        await bot.send_message(chat_id, f'😪 | {name}, вы проиграли {c2}$ (x0) .', parse_mode='html') 
                        cursor.execute(f'UPDATE user SET balance = {balance - summ} where id = "{user_id}"')
                        cursor.execute(f'UPDATE user SET games = {games + 1} where id = "{user_id}"')
                        cursor.execute(f'UPDATE bots SET last_stavka=? WHERE chat_id=?', (time.time(), chat_id,)) 
                        connect.commit()   
                        return                           
                    if int(rx) in range(10,29):
                        c = Decimal(summ - summ * 0.25) 
                        c2 = round(c)
                        c2 = '{:,}'.format(c2)
                        await bot.send_message(chat_id, f'😪 | {name}, вы проиграли {c2}$ (x0.25) .', parse_mode='html')
                        cursor.execute(f'UPDATE user SET balance = {balance - summ * 0.75} where id = "{user_id}"')
                        cursor.execute(f'UPDATE user SET games = {games + 1} where id = "{user_id}"')
                        cursor.execute(f'UPDATE bots SET last_stavka=? WHERE chat_id=?', (time.time(), chat_id,))
                        connect.commit()  
                        return   
                    if int(rx) in range(30,44):
                        c = Decimal(summ * 0.5)
                        c2 = round(c)
                        c2 = '{:,}'.format(c2)
                        await bot.send_message(chat_id, f'😪 | {name}, вы проиграли {c2}$ (x0.5) .', parse_mode='html')
                        cursor.execute(f'UPDATE user SET balance = {balance - summ * 0.5} where id = "{user_id}"')
                        cursor.execute(f'UPDATE user SET games = {games + 1} where id = "{user_id}"')
                        cursor.execute(f'UPDATE bots SET last_stavka=? WHERE chat_id=?', (time.time(), chat_id,))
                        connect.commit() 
                        return  
                    if int(rx) in range(45,54):
                        c = Decimal(summ - summ * 0.75)
                        c2 = round(c)
                        c2 = '{:,}'.format(c2)
                        await bot.send_message(chat_id, f'😪 | {name}, вы проиграли {c2}$ (x0.75) .', parse_mode='html')
                        cursor.execute(f'UPDATE user SET balance = {balance - summ * 0.25} where id = "{user_id}"')
                        cursor.execute(f'UPDATE user SET games = {games + 1} where id = "{user_id}"')
                        cursor.execute(f'UPDATE bots SET last_stavka=? WHERE chat_id=?', (time.time(), chat_id,))
                        connect.commit() 
                        return  
                    if int(rx) in range(55,64):
                        c = summ * 1
                        c2 = round(c)
                        c2 = '{:,}'.format(c2)
                        await bot.send_message(chat_id, f'{name1}, ваши деньги остаются при вас {c2}$ (x1)  ', parse_mode='html')
                        cursor.execute(f'UPDATE bots SET last_stavka=? WHERE chat_id=?', (time.time(), chat_id,))
                        cursor.execute(f'UPDATE user SET games = {games + 1} where id = "{user_id}"')
                        connect.commit()
                        return 
                    if int(rx) in range(65,69):
                        c = Decimal(summ * 1.25)
                        c2 = round(c)
                        c2 = '{:,}'.format(c2)
                        await bot.send_message(chat_id, f'☘ | {name}, вы выиграли {c2}$ (x1.25)  ', parse_mode='html')       
                        cursor.execute(f'UPDATE user SET balance = {(balance - summ) + (summ * 1.25)} where id = "{user_id}"')
                        cursor.execute(f'UPDATE user SET games = {games + 1} where id = "{user_id}"')
                        cursor.execute(f'UPDATE bots SET last_stavka=? WHERE chat_id=?', (time.time(), chat_id,))
                        connect.commit()           
                        return 
                    if int(rx) in range(70,74):
                        c = Decimal(summ * 1.5)
                        c2 = round(c)
                        c2 = '{:,}'.format(c2)
                        await bot.send_message(chat_id, f'☘ | {name}, вы выиграли {c2}$ (x1.5)  ', parse_mode='html')
                        cursor.execute(f'UPDATE user SET balance = {(balance - summ) + (summ * 1.5)} where id = "{user_id}"')
                        cursor.execute(f'UPDATE user SET games = {games + 1} where id = "{user_id}"')
                        cursor.execute(f'UPDATE bots SET last_stavka=? WHERE chat_id=?', (time.time(), chat_id,))
                        connect.commit()  
                        return 
                    if int(rx) in range(75,84):
                        c = Decimal(summ * 1.75)
                        c2 = round(c)
                        c2 = '{:,}'.format(c2)
                        await bot.send_message(chat_id, f'☘ | {name}, вы выиграли {c2}$ (x1.75)  ', parse_mode='html')
                        cursor.execute(f'UPDATE user SET balance = {(balance - summ) + (summ * 1.75)} where id = "{user_id}"')
                        cursor.execute(f'UPDATE user SET games = {games + 1} where id = "{user_id}"')
                        cursor.execute(f'UPDATE bots SET last_stavka=? WHERE chat_id=?', (time.time(), chat_id,))
                        connect.commit()  
                        return 
                    if int(rx) in range(85,95):
                        c = Decimal(summ * 2)
                        c2 = round(c)
                        c2 = '{:,}'.format(c2)
                        await bot.send_message(chat_id, f'☘ | {name}, вы выиграли {c2}$ (x2)  ', parse_mode='html')
                        cursor.execute(f'UPDATE user SET balance = {(balance - summ) + (summ * 2)} where id = "{user_id}"')
                        cursor.execute(f'UPDATE user SET games = {games + 1} where id = "{user_id}"')
                        cursor.execute(f'UPDATE bots SET last_stavka=? WHERE chat_id=?', (time.time(), chat_id,))
                        connect.commit() 
                        return 
                    if int(rx) in range(100,108):
                        c = Decimal(summ * 3)
                        c2 = round(c)
                        c2 = '{:,}'.format(c2)
                        await bot.send_message(chat_id, f'☘ | {name}, вы выиграли {c2}$ (x3)  ', parse_mode='html')
                        cursor.execute(f'UPDATE user SET balance = {(balance - summ) + (summ * 3)} where id = "{user_id}"')
                        cursor.execute(f'UPDATE user SET games = {games + 1} where id = "{user_id}"')
                        cursor.execute(f'UPDATE bots SET last_stavka=? WHERE chat_id=?', (time.time(), chat_id,))
                        connect.commit() 
                        return 
                    if int(rx) == 109:
                        c = Decimal(summ * 5)
                        c2 = round(c)
                        c2 = '{:,}'.format(c2)
                        await bot.send_message(chat_id, f'☘ | {name}, вы выиграли {c2}$ (x5)  ', parse_mode='html')
                        cursor.execute(f'UPDATE user SET balance = {(balance - summ) + (summ * 5)} where id = "{user_id}"')
                        cursor.execute(f'UPDATE user SET games = {games + 1} where id = "{user_id}"')
                        cursor.execute(f'UPDATE bots SET last_stavka=? WHERE chat_id=?', (time.time(), chat_id,))
                        connect.commit() 
                        if int(rx) == 100:
                            c = Decimal(summ * 10)
                            c2 = round(c)
                            c2 = '{:,}'.format(c2)
                            await bot.send_message(chat_id, f'☘ | {name}, вы выиграли {c2}$ (x10)  ', parse_mode='html')
                            cursor.execute(f'UPDATE user SET balance = {(balance - summ) + (summ * 10)} where id = "{user_id}"')
                            cursor.execute(f'UPDATE user SET games = {games + 1} where id = "{user_id}"')
                            cursor.execute(f'UPDATE bots SET last_stavka=? WHERE chat_id=?', (time.time(), chat_id,))
                            connect.commit() 
                            return 
                elif summ <= 0:
                    await bot.send_message(chat_id, f'0⃣❌ | {name} нельзя ставить отрицательное число ', parse_mode='html')                                                       
            elif int(balance) <= int(summ):
                await bot.send_message(chat_id, f'😞 | Недостаточно средств', parse_mode='html')
        else:
            await bot.send_message(chat_id, f'⏱ | {name}, играть можно каждые 5 секунд!', parse_mode='html')
            return

# риск 
    if message.text.startswith("риск"):
        msg = message 
        user_id = msg.from_user.id
        name = message.from_user.get_mention(as_html=True)
        buttons_risk = InlineKeyboardMarkup(row_width=1)
        risk = InlineKeyboardButton(text='Готов(-а) рискнуть 🤯', callback_data='risk')
        remove_risk = InlineKeyboardButton(text='Удалить 🗑', callback_data='remove_risk')
        buttons_risk.add(risk, remove_risk)
        await message.reply(f"{name}, я смотрю на твое бесстрашие и удивляюсь 😳\n\n Но готов(-а) ли ты пойти до конца? 😱", reply_markup=buttons_risk, parse_mode='html')

# игры с эмоджи
    if message.text.startswith("гол"):
        msg = message 
        user_id = msg.from_user.id
        chat_id = message.chat.id
        name = message.from_user.get_mention(as_html=True)
        summ = int(msg.text.split()[1])
        games = cursor.execute("SELECT games from user where id = ?", (message.from_user.id,)).fetchone()
        games = int(games[0])
        balance = cursor.execute("SELECT balance from user where id = ?", (message.from_user.id,)).fetchone()
        balance = int(balance[0])
        period = 5
        get = cursor.execute("SELECT last_stavka FROM bots WHERE chat_id = ?", (message.chat.id,)).fetchone()
        last_stavka = f"{int(get[0])}"
        stavkatime = time.time() - float(last_stavka)
        checking = cursor.execute("SELECT checking from user WHERE id = ?", (message.from_user.id,)).fetchone()
        checking = round(int(checking[0]))
        if checking == 1:
            await bot.send_message(chat_id, f'⏱ | Пожалуйста, подождите конца игры', parse_mode='html')
            return 
        checking1 = cursor.execute("SELECT checking1 from user WHERE id = ?", (message.from_user.id,)).fetchone()
        checking1 = round(int(checking1[0]))
        if checking1 == 1:
            await bot.send_message(chat_id, f'⏱ | Пожалуйста, подождите конца игры', parse_mode='html')
            return
        checking2 = cursor.execute("SELECT checking2 from user WHERE id = ?", (message.from_user.id,)).fetchone()
        checking2 = round(int(checking2[0]))
        if checking2 == 1:
            await bot.send_message(chat_id, f'⏱ | Пожалуйста, подождите конца игры', parse_mode='html')
            return
        checking3 = cursor.execute("SELECT checking3 from user WHERE id = ?", (message.from_user.id,)).fetchone()
        checking3 = round(int(checking3[0]))
        if checking3 == 1:
            await bot.send_message(chat_id, f'⏱ | Пожалуйста, подождите конца игры', parse_mode='html')
            return 
        if stavkatime > period:
            if balance >= summ:
                if summ > 0:
                    dice_mes = await message.answer_dice(emoji='⚽️')
                    value = dice_mes.dice.value 
                    if value in [1, 2]:
                        await bot.send_message(message.chat.id, f"🙁 | {name}, вы промахнулись и проиграли {summ}$", parse_mode='html')
                        cursor.execute(f'UPDATE user SET balance = {(balance - summ)} where id = "{user_id}"')
                        cursor.execute(f'UPDATE user SET games = {games + 1} where id = "{user_id}"')
                        cursor.execute(f'UPDATE bots SET last_stavka=? WHERE chat_id=?', (time.time(), chat_id,))
                        connect.commit() 
                        return 
                    elif value in [3, 4, 5]:
                        await bot.send_message(message.chat.id, f"⭐️ | {name}, забивает прекрасный гол +{summ}$", parse_mode='html')
                        cursor.execute(f'UPDATE user SET balance = {(balance - summ)} where id = "{user_id}"')
                        cursor.execute(f'UPDATE user SET games = {games + 1} where id = "{user_id}"')
                        cursor.execute(f'UPDATE bots SET last_stavka=? WHERE chat_id=?', (time.time(), chat_id,))
                        connect.commit() 
                        return 
                elif summ <= 0:
                    await bot.send_message(chat_id, f'0⃣❌ | {name} нельзя ставить отрицательное число ', parse_mode='html') 
            elif int(balance) <= int(summ):
                await bot.send_message(chat_id, f'😞 | Недостаточно средств', parse_mode='html')
        else:
            await bot.send_message(chat_id, f'⏱ | {name}, играть можно каждые 5 секунд!', parse_mode='html')
            return
            

    if message.text.startswith("Гол"):
        msg = message 
        user_id = msg.from_user.id
        chat_id = message.chat.id
        name = message.from_user.get_mention(as_html=True)
        summ = int(msg.text.split()[1])
        games = cursor.execute("SELECT games from user where id = ?", (message.from_user.id,)).fetchone()
        games = int(games[0])
        balance = cursor.execute("SELECT balance from user where id = ?", (message.from_user.id,)).fetchone()
        balance = int(balance[0])
        period = 5
        get = cursor.execute("SELECT last_stavka FROM bots WHERE chat_id = ?", (message.chat.id,)).fetchone()
        last_stavka = f"{int(get[0])}"
        stavkatime = time.time() - float(last_stavka)
        checking = cursor.execute("SELECT checking from user WHERE id = ?", (message.from_user.id,)).fetchone()
        checking = round(int(checking[0]))
        if checking == 1:
            await bot.send_message(chat_id, f'⏱ | Пожалуйста, подождите конца игры', parse_mode='html')
            return 
        checking1 = cursor.execute("SELECT checking1 from user WHERE id = ?", (message.from_user.id,)).fetchone()
        checking1 = round(int(checking1[0]))
        if checking1 == 1:
            await bot.send_message(chat_id, f'⏱ | Пожалуйста, подождите конца игры', parse_mode='html')
            return
        checking2 = cursor.execute("SELECT checking2 from user WHERE id = ?", (message.from_user.id,)).fetchone()
        checking2 = round(int(checking2[0]))
        if checking2 == 1:
            await bot.send_message(chat_id, f'⏱ | Пожалуйста, подождите конца игры', parse_mode='html')
            return
        checking3 = cursor.execute("SELECT checking3 from user WHERE id = ?", (message.from_user.id,)).fetchone()
        checking3 = round(int(checking3[0]))
        if checking3 == 1:
            await bot.send_message(chat_id, f'⏱ | Пожалуйста, подождите конца игры', parse_mode='html')
            return 
        if stavkatime > period:
            if balance >= summ:
                if summ > 0:
                    dice_mes = await message.answer_dice(emoji='⚽️')
                    value = dice_mes.dice.value 
                    if value in [1, 2]:
                        await bot.send_message(message.chat.id, f"🙁 | {name}, вы промахнулись и проиграли {summ}$", parse_mode='html')
                        cursor.execute(f'UPDATE user SET balance = {(balance - summ)} where id = "{user_id}"')
                        cursor.execute(f'UPDATE user SET games = {games + 1} where id = "{user_id}"')
                        cursor.execute(f'UPDATE bots SET last_stavka=? WHERE chat_id=?', (time.time(), chat_id,))
                        connect.commit() 
                        return 
                    elif value in [3, 4, 5]:
                        await bot.send_message(message.chat.id, f"⭐️ | {name}, забивает прекрасный гол +{summ}$", parse_mode='html')
                        cursor.execute(f'UPDATE user SET balance = {(balance - summ)} where id = "{user_id}"')
                        cursor.execute(f'UPDATE user SET games = {games + 1} where id = "{user_id}"')
                        cursor.execute(f'UPDATE bots SET last_stavka=? WHERE chat_id=?', (time.time(), chat_id,))
                        connect.commit() 
                        return 
                elif summ <= 0:
                    await bot.send_message(chat_id, f'0⃣❌ | {name} нельзя ставить отрицательное число ', parse_mode='html') 
            elif int(balance) <= int(summ):
                await bot.send_message(chat_id, f'😞 | Недостаточно средств', parse_mode='html')
        else:
            await bot.send_message(chat_id, f'⏱ | {name}, играть можно каждые 5 секунд!', parse_mode='html')
            return

    if message.text.startswith("куб"):
        msg = message 
        user_id = msg.from_user.id
        chat_id = message.chat.id
        name = message.from_user.get_mention(as_html=True)
        isxod = int(msg.text.split()[1])
        summ = int(msg.text.split()[2])
        games = cursor.execute("SELECT games from user where id = ?", (message.from_user.id,)).fetchone()
        games = int(games[0])
        balance = cursor.execute("SELECT balance from user where id = ?", (message.from_user.id,)).fetchone()
        balance = int(balance[0])
        period = 5
        get = cursor.execute("SELECT last_stavka FROM bots WHERE chat_id = ?", (message.chat.id,)).fetchone()
        last_stavka = f"{int(get[0])}"
        stavkatime = time.time() - float(last_stavka)
        checking = cursor.execute("SELECT checking from user WHERE id = ?", (message.from_user.id,)).fetchone()
        checking = round(int(checking[0]))
        if checking == 1:
            await bot.send_message(chat_id, f'⏱ | Пожалуйста, подождите конца игры', parse_mode='html')
            return 
        checking1 = cursor.execute("SELECT checking1 from user WHERE id = ?", (message.from_user.id,)).fetchone()
        checking1 = round(int(checking1[0]))
        if checking1 == 1:
            await bot.send_message(chat_id, f'⏱ | Пожалуйста, подождите конца игры', parse_mode='html')
            return
        checking2 = cursor.execute("SELECT checking2 from user WHERE id = ?", (message.from_user.id,)).fetchone()
        checking2 = round(int(checking2[0]))
        if checking2 == 1:
            await bot.send_message(chat_id, f'⏱ | Пожалуйста, подождите конца игры', parse_mode='html')
            return
        checking3 = cursor.execute("SELECT checking3 from user WHERE id = ?", (message.from_user.id,)).fetchone()
        checking3 = round(int(checking3[0]))
        if checking3 == 1:
            await bot.send_message(chat_id, f'⏱ | Пожалуйста, подождите конца игры', parse_mode='html')
            return 
        if isxod <= 6 and isxod >= 1:
            if stavkatime > period:
                if balance >= summ:
                    if summ > 0:
                        dice_mes = await bot.send_dice(message.chat.id)
                        value = dice_mes.dice.value 
                        if value == isxod:
                            await bot.send_message(message.chat.id, f"🎊 | {name}, нам повезло и кубик выпал на то число что ты загадал(-а)\n Ваш приз: {summ*3}$", parse_mode='html')
                            cursor.execute(f'UPDATE user SET balance = {(balance + summ + summ + summ)} where id = "{user_id}"')
                            cursor.execute(f'UPDATE user SET games = {games + 1} where id = "{user_id}"')
                            cursor.execute(f'UPDATE bots SET last_stavka=? WHERE chat_id=?', (time.time(), chat_id,))
                            connect.commit()
                            return 
                        else:
                            await bot.send_message(message.chat.id, f"🙁 | {name}, удача сегодня не с вами, вы проиорали {summ}$", parse_mode='html')
                            cursor.execute(f'UPDATE user SET balance = {(balance - summ)} where id = "{user_id}"')
                            cursor.execute(f'UPDATE user SET games = {games + 1} where id = "{user_id}"')
                            cursor.execute(f'UPDATE bots SET last_stavka=? WHERE chat_id=?', (time.time(), chat_id,))
                            connect.commit() 
                            return 
                    elif summ <= 0:
                        await bot.send_message(chat_id, f'0⃣❌ | {name} нельзя ставить отрицательное число ', parse_mode='html') 
                elif int(balance) <= int(summ):
                    await bot.send_message(chat_id, f'😞 | Недостаточно средств', parse_mode='html')
            else:
                await bot.send_message(chat_id, f'⏱ | {name}, играть можно каждые 5 секунд!', parse_mode='html')
                return
        else:
            await message.reply(f"Число должно быть от 1 до 6.")

    if message.text.startswith("Куб"):
        msg = message 
        user_id = msg.from_user.id
        chat_id = message.chat.id
        name = message.from_user.get_mention(as_html=True)
        isxod = int(msg.text.split()[1])
        summ = int(msg.text.split()[2])
        games = cursor.execute("SELECT games from user where id = ?", (message.from_user.id,)).fetchone()
        games = int(games[0])
        balance = cursor.execute("SELECT balance from user where id = ?", (message.from_user.id,)).fetchone()
        balance = int(balance[0])
        period = 5
        get = cursor.execute("SELECT last_stavka FROM bots WHERE chat_id = ?", (message.chat.id,)).fetchone()
        last_stavka = f"{int(get[0])}"
        stavkatime = time.time() - float(last_stavka)
        checking = cursor.execute("SELECT checking from user WHERE id = ?", (message.from_user.id,)).fetchone()
        checking = round(int(checking[0]))
        if checking == 1:
            await bot.send_message(chat_id, f'⏱ | Пожалуйста, подождите конца игры', parse_mode='html')
            return 
        checking1 = cursor.execute("SELECT checking1 from user WHERE id = ?", (message.from_user.id,)).fetchone()
        checking1 = round(int(checking1[0]))
        if checking1 == 1:
            await bot.send_message(chat_id, f'⏱ | Пожалуйста, подождите конца игры', parse_mode='html')
            return
        checking2 = cursor.execute("SELECT checking2 from user WHERE id = ?", (message.from_user.id,)).fetchone()
        checking2 = round(int(checking2[0]))
        if checking2 == 1:
            await bot.send_message(chat_id, f'⏱ | Пожалуйста, подождите конца игры', parse_mode='html')
            return
        checking3 = cursor.execute("SELECT checking3 from user WHERE id = ?", (message.from_user.id,)).fetchone()
        checking3 = round(int(checking3[0]))
        if checking3 == 1:
            await bot.send_message(chat_id, f'⏱ | Пожалуйста, подождите конца игры', parse_mode='html')
            return 
        if isxod <= 6 and isxod >= 1:
            if stavkatime > period:
                if balance >= summ:
                    if summ > 0:
                        dice_mes = await bot.send_dice(message.chat.id)
                        value = dice_mes.dice.value 
                        if value == isxod:
                            await bot.send_message(message.chat.id, f"🎊 | {name}, нам повезло и кубик выпал на то число что ты загадал(-а)\n Ваш приз: {summ*3}$", parse_mode='html')
                            cursor.execute(f'UPDATE user SET balance = {(balance + summ + summ + summ)} where id = "{user_id}"')
                            cursor.execute(f'UPDATE user SET games = {games + 1} where id = "{user_id}"')
                            cursor.execute(f'UPDATE bots SET last_stavka=? WHERE chat_id=?', (time.time(), chat_id,))
                            connect.commit()
                            return 
                        else:
                            await bot.send_message(message.chat.id, f"🙁 | {name}, удача сегодня не с вами, вы проиорали {summ}$", parse_mode='html')
                            cursor.execute(f'UPDATE user SET balance = {(balance - summ)} where id = "{user_id}"')
                            cursor.execute(f'UPDATE user SET games = {games + 1} where id = "{user_id}"')
                            cursor.execute(f'UPDATE bots SET last_stavka=? WHERE chat_id=?', (time.time(), chat_id,))
                            connect.commit() 
                            return 
                    elif summ <= 0:
                        await bot.send_message(chat_id, f'0⃣❌ | {name} нельзя ставить отрицательное число ', parse_mode='html') 
                elif int(balance) <= int(summ):
                    await bot.send_message(chat_id, f'😞 | Недостаточно средств', parse_mode='html')
            else:
                await bot.send_message(chat_id, f'⏱ | {name}, играть можно каждые 5 секунд!', parse_mode='html')
                return
        else:
            await message.reply(f"Число должно быть от 1 до 6.")

    if message.text.startswith("бас"):
        msg = message 
        user_id = msg.from_user.id
        chat_id = message.chat.id
        name = message.from_user.get_mention(as_html=True)
        summ = int(msg.text.split()[1])
        games = cursor.execute("SELECT games from user where id = ?", (message.from_user.id,)).fetchone()
        games = int(games[0])
        balance = cursor.execute("SELECT balance from user where id = ?", (message.from_user.id,)).fetchone()
        balance = int(balance[0])
        period = 5
        get = cursor.execute("SELECT last_stavka FROM bots WHERE chat_id = ?", (message.chat.id,)).fetchone()
        last_stavka = f"{int(get[0])}"
        stavkatime = time.time() - float(last_stavka)
        checking = cursor.execute("SELECT checking from user WHERE id = ?", (message.from_user.id,)).fetchone()
        checking = round(int(checking[0]))
        if checking == 1:
            await bot.send_message(chat_id, f'⏱ | Пожалуйста, подождите конца игры', parse_mode='html')
            return 
        checking1 = cursor.execute("SELECT checking1 from user WHERE id = ?", (message.from_user.id,)).fetchone()
        checking1 = round(int(checking1[0]))
        if checking1 == 1:
            await bot.send_message(chat_id, f'⏱ | Пожалуйста, подождите конца игры', parse_mode='html')
            return
        checking2 = cursor.execute("SELECT checking2 from user WHERE id = ?", (message.from_user.id,)).fetchone()
        checking2 = round(int(checking2[0]))
        if checking2 == 1:
            await bot.send_message(chat_id, f'⏱ | Пожалуйста, подождите конца игры', parse_mode='html')
            return
        checking3 = cursor.execute("SELECT checking3 from user WHERE id = ?", (message.from_user.id,)).fetchone()
        checking3 = round(int(checking3[0]))
        if checking3 == 1:
            await bot.send_message(chat_id, f'⏱ | Пожалуйста, подождите конца игры', parse_mode='html')
            return 
        if stavkatime > period:
            if balance >= summ:
                if summ > 0:
                    dice_mes = await message.answer_dice(emoji='🏀')
                    value = dice_mes.dice.value 
                    if value in [4, 5]:
                        await bot.send_message(message.chat.id, f"☄ | {name}, отличное попадание +{summ}$", parse_mode='html')
                        cursor.execute(f'UPDATE user SET balance = {(balance + summ)} where id = "{user_id}"')
                        cursor.execute(f'UPDATE user SET games = {games + 1} where id = "{user_id}"')
                        cursor.execute(f'UPDATE bots SET last_stavka=? WHERE chat_id=?', (time.time(), chat_id,))
                        connect.commit() 
                        return 
                    elif value in [1, 2, 3]:
                        await bot.send_message(message.chat.id, f"🙁 | {name}, вы промахнулись и проиграли {summ}$", parse_mode='html')
                        cursor.execute(f'UPDATE user SET balance = {(balance - summ)} where id = "{user_id}"')
                        cursor.execute(f'UPDATE user SET games = {games + 1} where id = "{user_id}"')
                        cursor.execute(f'UPDATE bots SET last_stavka=? WHERE chat_id=?', (time.time(), chat_id,))
                        connect.commit() 
                        return 
                elif summ <= 0:
                    await bot.send_message(chat_id, f'0⃣❌ | {name} нельзя ставить отрицательное число ', parse_mode='html') 
            elif int(balance) <= int(summ):
                await bot.send_message(chat_id, f'😞 | Недостаточно средств', parse_mode='html')
        else:
            await bot.send_message(chat_id, f'⏱ | {name}, играть можно каждые 5 секунд!', parse_mode='html')
            return

    if message.text.startswith("бас"):
        msg = message 
        user_id = msg.from_user.id
        chat_id = message.chat.id
        name = message.from_user.get_mention(as_html=True)
        summ = int(msg.text.split()[1])
        games = cursor.execute("SELECT games from user where id = ?", (message.from_user.id,)).fetchone()
        games = int(games[0])
        balance = cursor.execute("SELECT balance from user where id = ?", (message.from_user.id,)).fetchone()
        balance = int(balance[0])
        period = 5
        get = cursor.execute("SELECT last_stavka FROM bots WHERE chat_id = ?", (message.chat.id,)).fetchone()
        last_stavka = f"{int(get[0])}"
        stavkatime = time.time() - float(last_stavka)
        checking = cursor.execute("SELECT checking from user WHERE id = ?", (message.from_user.id,)).fetchone()
        checking = round(int(checking[0]))
        if checking == 1:
            await bot.send_message(chat_id, f'⏱ | Пожалуйста, подождите конца игры', parse_mode='html')
            return 
        checking1 = cursor.execute("SELECT checking1 from user WHERE id = ?", (message.from_user.id,)).fetchone()
        checking1 = round(int(checking1[0]))
        if checking1 == 1:
            await bot.send_message(chat_id, f'⏱ | Пожалуйста, подождите конца игры', parse_mode='html')
            return
        checking2 = cursor.execute("SELECT checking2 from user WHERE id = ?", (message.from_user.id,)).fetchone()
        checking2 = round(int(checking2[0]))
        if checking2 == 1:
            await bot.send_message(chat_id, f'⏱ | Пожалуйста, подождите конца игры', parse_mode='html')
            return
        checking3 = cursor.execute("SELECT checking3 from user WHERE id = ?", (message.from_user.id,)).fetchone()
        checking3 = round(int(checking3[0]))
        if checking3 == 1:
            await bot.send_message(chat_id, f'⏱ | Пожалуйста, подождите конца игры', parse_mode='html')
            return 
        if stavkatime > period:
            if balance >= summ:
                if summ > 0:
                    dice_mes = await message.answer_dice(emoji='🏀')
                    value = dice_mes.dice.value 
                    if value in [4, 5]:
                        await bot.send_message(message.chat.id, f"☄ | {name}, отличное попадание +{summ}$", parse_mode='html')
                        cursor.execute(f'UPDATE user SET balance = {(balance + summ)} where id = "{user_id}"')
                        cursor.execute(f'UPDATE user SET games = {games + 1} where id = "{user_id}"')
                        cursor.execute(f'UPDATE bots SET last_stavka=? WHERE chat_id=?', (time.time(), chat_id,))
                        connect.commit() 
                        return 
                    elif value in [1, 2, 3]:
                        await bot.send_message(message.chat.id, f"🙁 | {name}, вы промахнулись и проиграли {summ}$", parse_mode='html')
                        cursor.execute(f'UPDATE user SET balance = {(balance - summ)} where id = "{user_id}"')
                        cursor.execute(f'UPDATE user SET games = {games + 1} where id = "{user_id}"')
                        cursor.execute(f'UPDATE bots SET last_stavka=? WHERE chat_id=?', (time.time(), chat_id,))
                        connect.commit() 
                        return 
                elif summ <= 0:
                    await bot.send_message(chat_id, f'0⃣❌ | {name} нельзя ставить отрицательное число ', parse_mode='html') 
            elif int(balance) <= int(summ):
                await bot.send_message(chat_id, f'😞 | Недостаточно средств', parse_mode='html')
        else:
            await bot.send_message(chat_id, f'⏱ | {name}, играть можно каждые 5 секунд!', parse_mode='html')
            return

    if message.text.startswith("боул"):
        msg = message 
        user_id = msg.from_user.id
        chat_id = message.chat.id
        name = message.from_user.get_mention(as_html=True)
        summ = int(msg.text.split()[1])
        games = cursor.execute("SELECT games from user where id = ?", (message.from_user.id,)).fetchone()
        games = int(games[0])
        balance = cursor.execute("SELECT balance from user where id = ?", (message.from_user.id,)).fetchone()
        balance = int(balance[0])
        period = 5
        get = cursor.execute("SELECT last_stavka FROM bots WHERE chat_id = ?", (message.chat.id,)).fetchone()
        last_stavka = f"{int(get[0])}"
        stavkatime = time.time() - float(last_stavka)
        checking = cursor.execute("SELECT checking from user WHERE id = ?", (message.from_user.id,)).fetchone()
        checking = round(int(checking[0]))
        if checking == 1:
            await bot.send_message(chat_id, f'⏱ | Пожалуйста, подождите конца игры', parse_mode='html')
            return 
        checking1 = cursor.execute("SELECT checking1 from user WHERE id = ?", (message.from_user.id,)).fetchone()
        checking1 = round(int(checking1[0]))
        if checking1 == 1:
            await bot.send_message(chat_id, f'⏱ | Пожалуйста, подождите конца игры', parse_mode='html')
            return
        checking2 = cursor.execute("SELECT checking2 from user WHERE id = ?", (message.from_user.id,)).fetchone()
        checking2 = round(int(checking2[0]))
        if checking2 == 1:
            await bot.send_message(chat_id, f'⏱ | Пожалуйста, подождите конца игры', parse_mode='html')
            return
        checking3 = cursor.execute("SELECT checking3 from user WHERE id = ?", (message.from_user.id,)).fetchone()
        checking3 = round(int(checking3[0]))
        if checking3 == 1:
            await bot.send_message(chat_id, f'⏱ | Пожалуйста, подождите конца игры', parse_mode='html')
            return 
        if stavkatime > period:
            if balance >= summ:
                if summ > 0:
                    dice_mes = await message.answer_dice(emoji='🎳')
                    value = dice_mes.dice.value 
                    if value in [4, 5, 6]:
                        await bot.send_message(message.chat.id, f"🎆 | {name}, отличный бросок +{summ}$", parse_mode='html')
                        cursor.execute(f'UPDATE user SET balance = {(balance + summ)} where id = "{user_id}"')
                        cursor.execute(f'UPDATE user SET games = {games + 1} where id = "{user_id}"')
                        cursor.execute(f'UPDATE bots SET last_stavka=? WHERE chat_id=?', (time.time(), chat_id,))
                        connect.commit() 
                        return 
                    elif value in [1, 2, 3]:
                        await bot.send_message(message.chat.id, f"🙁 | {name}, не очень удачный бросок, вы проиграли {summ}$", parse_mode='html')
                        cursor.execute(f'UPDATE user SET balance = {(balance - summ)} where id = "{user_id}"')
                        cursor.execute(f'UPDATE user SET games = {games + 1} where id = "{user_id}"')
                        cursor.execute(f'UPDATE bots SET last_stavka=? WHERE chat_id=?', (time.time(), chat_id,))
                        connect.commit() 
                        return 
                elif summ <= 0:
                    await bot.send_message(chat_id, f'0⃣❌ | {name} нельзя ставить отрицательное число ', parse_mode='html') 
            elif int(balance) <= int(summ):
                await bot.send_message(chat_id, f'😞 | Недостаточно средств', parse_mode='html')
        else:
            await bot.send_message(chat_id, f'⏱ | {name}, играть можно каждые 5 секунд!', parse_mode='html')
            return

# передача монет
    if message.text.startswith("дать"):
        msg = message
        user_id = msg.from_user.id
        name = msg.from_user.last_name 
        rname =  msg.reply_to_message.from_user.last_name 
        user_name = message.from_user.get_mention(as_html=True)
        reply_user_name = message.reply_to_message.from_user.get_mention(as_html=True)
        reply_user_id = msg.reply_to_message.from_user.id
       
        perevod = int(msg.text.split()[1])
        perevod2 = '{:,}'.format(perevod)

        cursor.execute(f"SELECT id FROM user WHERE id = '{user_id}'")
        balance = cursor.execute("SELECT balance from user WHERE id = ?", (message.from_user.id,)).fetchone()
        balance = round(int(balance[0]))
        balance2 = cursor.execute("SELECT balance from user WHERE id = ?", (message.reply_to_message.from_user.id,)).fetchone()
        balance2 = round(balance2[0])
        checking = cursor.execute("SELECT checking from user WHERE id = ?", (message.from_user.id,)).fetchone()
        checking = round(int(checking[0]))

        if not reply_user_id:
            await message.reply("❗ | Повторите передачу, но с реплаем на человека которому хотите передать.")
            return
       
        if reply_user_id == user_id:
            await message.reply(f'🩳 | Переложили деньги с одного кармана в другой', parse_mode='html')
            return

        if reply_user_id == (await bot.get_me()).id:
            await message.reply(f"Нельзя передать что либо боту.")
            return

        if checking == 1:
            await bot.send_message(chat_id, f'⏱ | Пожалуйста, подождите конца игры', parse_mode='html')
            return 
        checking1 = cursor.execute("SELECT checking1 from user WHERE id = ?", (message.from_user.id,)).fetchone()
        checking1 = round(int(checking1[0]))
        if checking1 == 1:
            await bot.send_message(chat_id, f'⏱ | Пожалуйста, подождите конца игры', parse_mode='html')
            return
        checking2 = cursor.execute("SELECT checking2 from user WHERE id = ?", (message.from_user.id,)).fetchone()
        checking2 = round(int(checking2[0]))
        if checking2 == 1:
            await bot.send_message(chat_id, f'⏱ | Пожалуйста, подождите конца игры', parse_mode='html')
            return
        checking3 = cursor.execute("SELECT checking3 from user WHERE id = ?", (message.from_user.id,)).fetchone()
        checking3 = round(int(checking3[0]))
        if checking3 == 1:
            await bot.send_message(chat_id, f'⏱ | Пожалуйста, подождите конца игры', parse_mode='html')
            return

        if perevod > 0:
            if balance >= perevod:
                await message.reply(f'🔃 | Передал(-а) {perevod2}$, {reply_user_name}', parse_mode='html')
                cursor.execute(f'UPDATE user SET balance = {balance - perevod} WHERE id = "{user_id}"') 
                cursor.execute(f'UPDATE user SET balance = {balance2 + perevod} WHERE id = "{reply_user_id}"')
                connect.commit()    
   
            elif int(balance) <= int(perevod):
                await message.reply( f'🔃❌ | {user_name} недостаточно средств для передачи.', parse_mode='html')

        if perevod <= 0:
            await message.reply( f'0⃣❌ | Нельзя передать отрицательное число', parse_mode='html')  

    if message.text.startswith("Дать"):
        msg = message
        user_id = msg.from_user.id
        name = msg.from_user.last_name 
        rname =  msg.reply_to_message.from_user.last_name 
        user_name = message.from_user.get_mention(as_html=True)
        reply_user_name = message.reply_to_message.from_user.get_mention(as_html=True)
        reply_user_id = msg.reply_to_message.from_user.id
       
        perevod = int(msg.text.split()[1])
        perevod2 = '{:,}'.format(perevod)

        cursor.execute(f"SELECT id FROM user WHERE id = '{user_id}'")
        balance = cursor.execute("SELECT balance from user WHERE id = ?", (message.from_user.id,)).fetchone()
        balance = round(int(balance[0]))
        balance2 = cursor.execute("SELECT balance from user WHERE id = ?", (message.reply_to_message.from_user.id,)).fetchone()
        balance2 = round(balance2[0])
        checking = cursor.execute("SELECT checking from user WHERE id = ?", (message.from_user.id,)).fetchone()
        checking = round(int(checking[0]))

        if not reply_user_id:
            await message.reply("❗ | Повторите передачу, но с реплаем на человека которому хотите передать.")
            return
       
        if reply_user_id == user_id:
            await message.reply(f'🩳 | Переложили деньги с одного кармана в другой', parse_mode='html')
            return

        if reply_user_id == (await bot.get_me()).id:
            await message.reply(f"Нельзя передать что либо боту.")
            return

        if checking == 1:
            await bot.send_message(chat_id, f'⏱ | Пожалуйста, подождите конца игры', parse_mode='html')
            return 
        checking1 = cursor.execute("SELECT checking1 from user WHERE id = ?", (message.from_user.id,)).fetchone()
        checking1 = round(int(checking1[0]))
        if checking1 == 1:
            await bot.send_message(chat_id, f'⏱ | Пожалуйста, подождите конца игры', parse_mode='html')
            return
        checking2 = cursor.execute("SELECT checking2 from user WHERE id = ?", (message.from_user.id,)).fetchone()
        checking2 = round(int(checking2[0]))
        if checking2 == 1:
            await bot.send_message(chat_id, f'⏱ | Пожалуйста, подождите конца игры', parse_mode='html')
            return
        checking3 = cursor.execute("SELECT checking3 from user WHERE id = ?", (message.from_user.id,)).fetchone()
        checking3 = round(int(checking3[0]))
        if checking3 == 1:
            await bot.send_message(chat_id, f'⏱ | Пожалуйста, подождите конца игры', parse_mode='html')
            return

        if perevod > 0:
            if balance >= perevod:
                await message.reply(f'🔃 | Передал(-а) {perevod2}$, {reply_user_name}', parse_mode='html')
                cursor.execute(f'UPDATE user SET balance = {balance - perevod} WHERE id = "{user_id}"') 
                cursor.execute(f'UPDATE user SET balance = {balance2 + perevod} WHERE id = "{reply_user_id}"')
                connect.commit()    
   
            elif int(balance) <= int(perevod):
                await message.reply( f'🔃❌ | {user_name} недостаточно средств для передачи.', parse_mode='html')

        if perevod <= 0:
            await message.reply( f'0⃣❌ | Нельзя передать отрицательное число', parse_mode='html') 

# рп команды
    if message.text.lower() == "чмок": 
        user_name = message.from_user.get_mention(as_html=True) 
        reply_user_name = message.reply_to_message.from_user.get_mention(as_html=True) 
        reply = message.reply_to_message 
        if reply: 
            replyuser = reply.from_user 
            await bot.send_message(message.chat.id, f"💋 | {user_name} чмокнул(-а) {reply_user_name}", parse_mode='html') 
    if message.text.lower() == "кусь": 
        user_name = message.from_user.get_mention(as_html=True) 
        reply_user_name = message.reply_to_message.from_user.get_mention(as_html=True) 
        reply = message.reply_to_message 
        if reply: 
            replyuser = reply.from_user 
            await bot.send_message(message.chat.id, f"😼 | {user_name} кусьнул(-а) {reply_user_name}", parse_mode='html') 
    if message.text.lower() == "обнять": 
        user_name = message.from_user.get_mention(as_html=True) 
        reply_user_name = message.reply_to_message.from_user.get_mention(as_html=True) 
        reply = message.reply_to_message 
        if reply: 
            replyuser = reply.from_user 
            await bot.send_message(message.chat.id, f"🤗 | {user_name} обнял(-а) {reply_user_name}", parse_mode='html') 
    if message.text.lower() == "поцеловать": 
        user_name = message.from_user.get_mention(as_html=True) 
        reply_user_name = message.reply_to_message.from_user.get_mention(as_html=True) 
        reply = message.reply_to_message 
        if reply: 
            replyuser = reply.from_user 
            await bot.send_message(message.chat.id, f"💋 | {user_name} поцеловал(-а) {reply_user_name}", parse_mode='html') 
    if message.text.lower() == "дать пять": 
        user_name = message.from_user.get_mention(as_html=True) 
        reply_user_name = message.reply_to_message.from_user.get_mention(as_html=True) 
        reply = message.reply_to_message 
        if reply: 
            replyuser = reply.from_user 
            await bot.send_message(message.chat.id, f"✋ | {user_name} дал(-а) пять {reply_user_name}", parse_mode='html') 
    if message.text.lower() == "подарить айфон": 
        user_name = message.from_user.get_mention(as_html=True) 
        reply_user_name = message.reply_to_message.from_user.get_mention(as_html=True) 
        reply = message.reply_to_message 
        if reply: 
            replyuser = reply.from_user 
            await bot.send_message(message.chat.id, f"📱 | {user_name} подарил(-а) айфон {reply_user_name}", parse_mode='html') 
    if message.text.lower() == "ударить": 
        user_name = message.from_user.get_mention(as_html=True) 
        reply_user_name = message.reply_to_message.from_user.get_mention(as_html=True) 
        reply = message.reply_to_message 
        if reply: 
            replyuser = reply.from_user 
            await bot.send_message(message.chat.id, f"🤛 | {user_name} ударил(-а) {reply_user_name}", parse_mode='html') 
    if message.text.lower() == "заскамить": 
        user_name = message.from_user.get_mention(as_html=True)
        reply_user_name = message.reply_to_message.from_user.get_mention(as_html=True) 
        reply = message.reply_to_message 
        if reply: 
            replyuser = reply.from_user 
            await bot.send_message(message.chat.id, f"👨‍💻 | {user_name} заскамил(-а) {reply_user_name}", parse_mode='html') 
    if message.text.lower() == "прижать": 
        user_name = message.from_user.get_mention(as_html=True) 
        reply_user_name = message.reply_to_message.from_user.get_mention(as_html=True) 
        reply = message.reply_to_message 
        if reply: 
            replyuser = reply.from_user 
            await bot.send_message(message.chat.id, f"🤲 | {user_name} прижал(-а) {reply_user_name}", parse_mode='html') 
    if message.text.lower() == "укусить": 
        user_name = message.from_user.get_mention(as_html=True) 
        reply_user_name = message.reply_to_message.from_user.get_mention(as_html=True) 
        reply = message.reply_to_message 
        if reply: 
            replyuser = reply.from_user 
            await bot.send_message(message.chat.id, f"😬 | {user_name} укусил(-а) {reply_user_name}", parse_mode='html') 
    if message.text.lower() == "взять за руку": 
        user_name = message.from_user.get_mention(as_html=True) 
        reply_user_name = message.reply_to_message.from_user.get_mention(as_html=True) 
        reply = message.reply_to_message 
        if reply: 
            replyuser = reply.from_user 
            await bot.send_message(message.chat.id, f"🤝 | {user_name} взял(-а) за руку {reply_user_name}", parse_mode='html') 
    if message.text.lower() == "прижать": 
        user_name = message.from_user.get_mention(as_html=True) 
        reply_user_name = message.reply_to_message.from_user.get_mention(as_html=True) 
        reply = message.reply_to_message 
        if reply: 
            replyuser = reply.from_user 
            await bot.send_message(message.chat.id, f"🤲 | {user_name} прижал(-а) {reply_user_name}", parse_mode='html') 
    if message.text.lower() == "похлопать": 
        user_name = message.from_user.get_mention(as_html=True) 
        reply_user_name = message.reply_to_message.from_user.get_mention(as_html=True) 
        reply = message.reply_to_message 
        if reply: 
            replyuser = reply.from_user 
            await bot.send_message(message.chat.id, f"👏 | {user_name} похлопал(-а) {reply_user_name}", parse_mode='html') 
    if message.text.lower() == "изнасиловать":
        user_name = message.from_user.get_mention(as_html=True) 
        reply_user_name = message.reply_to_message.from_user.get_mention(as_html=True) 
        reply = message.reply_to_message 
        if reply: 
            replyuser = reply.from_user 
            await bot.send_message(message.chat.id, f"👉👌 | {user_name} изнасиловал(-а) {reply_user_name}", parse_mode='html') 
    if message.text.lower() == "пригласить на чай": 
        user_name = message.from_user.get_mention(as_html=True) 
        reply_user_name = message.reply_to_message.from_user.get_mention(as_html=True) 
        reply = message.reply_to_message 
        if reply: 
            replyuser = reply.from_user 
            await bot.send_message(message.chat.id, f"☕️ | {user_name} пригласил(-а) на чай {reply_user_name}", parse_mode='html') 
    if message.text.lower() == "убить": 
        user_name = message.from_user.get_mention(as_html=True) 
        reply_user_name = message.reply_to_message.from_user.get_mention(as_html=True) 
        reply = message.reply_to_message 
        if reply: 
            replyuser = reply.from_user 
            await bot.send_message(message.chat.id, f"🔪 | {user_name} убил(-а) {reply_user_name}", parse_mode='html') 
            
    if message.text.lower() == "уебать":
        user_name = message.from_user.get_mention(as_html=True) 
        reply_user_name = message.reply_to_message.from_user.get_mention(as_html=True) 
        reply = message.reply_to_message 
        if reply:
             replyuser = reply.from_user 
             await bot.send_message(message.chat.id, f"🤜 | {user_name} уебал(-а) {reply_user_name}", parse_mode='html') 
    if message.text.lower() == "украсть": 
        user_name = message.from_user.get_mention(as_html=True) 
        reply_user_name = message.reply_to_message.from_user.get_mention(as_html=True) 
        reply = message.reply_to_message 
        if reply: 
            replyuser = reply.from_user 
            await bot.send_message(message.chat.id, f"💰 | {user_name} украл(-а) у {reply_user_name} деньги", parse_mode='html') 
    if message.text.lower() == "отсосать": 
        user_name = message.from_user.get_mention(as_html=True) 
        reply_user_name = message.reply_to_message.from_user.get_mention(as_html=True) 
        reply = message.reply_to_message 
        if reply: 
            replyuser = reply.from_user 
            await bot.send_message(message.chat.id, f"🍌 | {user_name} отсосал(-а) {reply_user_name}", parse_mode='html') 
 
    if message.text.lower() == "отлизать": 
        user_name = message.from_user.get_mention(as_html=True) 
        reply_user_name = message.reply_to_message.from_user.get_mention(as_html=True) 
        reply = message.reply_to_message 
        if reply: 
            replyuser = reply.from_user 
            await bot.send_message(message.chat.id, f"👅 | {user_name} отлизал(-а) {reply_user_name}", parse_mode='html') 
 
    if message.text.lower() == "выебать": 
        user_name = message.from_user.get_mention(as_html=True) 
        reply_user_name = message.reply_to_message.from_user.get_mention(as_html=True) 
        reply = message.reply_to_message 
        if reply: 
            replyuser = reply.from_user 
            await bot.send_message(message.chat.id, f"🔞 | {user_name} выебал(-а) {reply_user_name}", parse_mode='html') 
 
    if message.text.lower() == "сжечь": 
        user_name = message.from_user.get_mention(as_html=True) 
        reply_user_name = message.reply_to_message.from_user.get_mention(as_html=True) 
        reply = message.reply_to_message 
        if reply: 
            replyuser = reply.from_user 
            await bot.send_message(message.chat.id, f"🔥 | {user_name} сжёг {reply_user_name}", parse_mode='html') 
 
    if message.text.lower() == "трахнуть": 
        user_name = message.from_user.get_mention(as_html=True) 
        reply_user_name = message.reply_to_message.from_user.get_mention(as_html=True) 
        reply = message.reply_to_message 
        if reply: 
            replyuser = reply.from_user 
            await bot.send_message(message.chat.id, f"🔞 | {user_name} трахнул(-а) {reply_user_name}", parse_mode='html')

    if message.text.lower() == "поздравить": 
        user_name = message.from_user.get_mention(as_html=True) 
        reply_user_name = message.reply_to_message.from_user.get_mention(as_html=True) 
        reply = message.reply_to_message 
        if reply: 
            replyuser = reply.from_user 
            await bot.send_message(message.chat.id, f"🥳 | {user_name} поздравил(-а) {reply_user_name}", parse_mode='html') 
    if message.text.lower() == "суициднуться":
        user_name = message.from_user.get_mention(as_html=True) 
        reply_user_name = message.reply_to_message.from_user.get_mention(as_html=True) 
        reply = message.reply_to_message 
        if reply: 
            replyuser = reply.from_user 
            await bot.send_message(message.chat.id, f"⚰ | {user_name} предложил(-а) {reply_user_name} суициднуться", parse_mode='html') 
    if message.text.lower() == "покушать": 
        user_name = message.from_user.get_mention(as_html=True) 
        reply_user_name = message.reply_to_message.from_user.get_mention(as_html=True) 
        reply = message.reply_to_message 
        if reply: 
            replyuser = reply.from_user 
            await bot.send_message(message.chat.id, f"🍟 | {user_name} позвал(-а) {reply_user_name} покушать", parse_mode='html') 
    if message.text.lower() == "вылечить": 
        user_name = message.from_user.get_mention(as_html=True) 
        reply_user_name = message.reply_to_message.from_user.get_mention(as_html=True) 
        reply = message.reply_to_message 
        if reply: 
            replyuser = reply.from_user 
            await bot.send_message(message.chat.id, f"😄 | {user_name} вылечил(-а) {reply_user_name} от тоски", parse_mode='html')
    if message.text.lower() == "завязать глаза": 
        user_name = message.from_user.get_mention(as_html=True) 
        reply_user_name = message.reply_to_message.from_user.get_mention(as_html=True) 
        reply = message.reply_to_message 
        if reply: 
            replyuser = reply.from_user 
            await bot.send_message(message.chat.id, f"🧣 | {user_name} завязал(-а) глаза {reply_user_name}", parse_mode='html') 
    if message.text.lower() == "помурчать": 
        user_name = message.from_user.get_mention(as_html=True) 
        reply_user_name = message.reply_to_message.from_user.get_mention(as_html=True) 
        reply = message.reply_to_message 
        if reply: 
            replyuser = reply.from_user 
            await bot.send_message(message.chat.id, f"🐈‍⬛ | {user_name} помурчал(-а) на ушко {reply_user_name}", parse_mode='html') 
    if message.text.lower() == "оглушить": 
        user_name = message.from_user.get_mention(as_html=True) 
        reply_user_name = message.reply_to_message.from_user.get_mention(as_html=True) 
        reply = message.reply_to_message 
        if reply: 
            replyuser = reply.from_user 
            await bot.send_message(message.chat.id, f"😵‍💫 | {user_name} оглушил(-а) арматурой {reply_user_name}", parse_mode='html') 
    if message.text.lower() == "показать ножки": 
        user_name = message.from_user.get_mention(as_html=True) 
        reply_user_name = message.reply_to_message.from_user.get_mention(as_html=True) 
        reply = message.reply_to_message 
        if reply: 
            replyuser = reply.from_user 
            await bot.send_message(message.chat.id, f"🙄 | {user_name} аккуратно покзал(-а)  {reply_user_name} ножки", parse_mode='html')
    if message.text.lower() == "заставить скинуть ручки": 
        user_name = message.from_user.get_mention(as_html=True) 
        reply_user_name = message.reply_to_message.from_user.get_mention(as_html=True) 
        reply = message.reply_to_message 
        if reply: 
            replyuser = reply.from_user 
            await bot.send_message(message.chat.id, f"🙊 | {user_name} заставил(-а) скинуть свои ручки {reply_user_name}", parse_mode='html') 
    if message.text.lower() == "заставить скинуть ножки": 
        user_name = message.from_user.get_mention(as_html=True) 
        reply_user_name = message.reply_to_message.from_user.get_mention(as_html=True) 
        reply = message.reply_to_message 
        if reply: 
            replyuser = reply.from_user 
            await bot.send_message(message.chat.id, f"🙊 | {user_name} заствил(-а) {reply_user_name} скинуть ножки в лс", parse_mode='html') 
    if message.text.lower() == "собрать алименты": 
        user_name = message.from_user.get_mention(as_html=True) 
        reply_user_name = message.reply_to_message.from_user.get_mention(as_html=True) 
        reply = message.reply_to_message 
        if reply: 
            replyuser = reply.from_user 
            await bot.send_message(message.chat.id, f"💰 | {user_name} собрал(-а) с  {reply_user_name} алименты", parse_mode='html') 
    if message.text.lower() == "прикусить губу": 
        user_name = message.from_user.get_mention(as_html=True) 
        reply_user_name = message.reply_to_message.from_user.get_mention(as_html=True) 
        reply = message.reply_to_message 
        if reply: 
            replyuser = reply.from_user 
            await bot.send_message(message.chat.id, f"🤭 | {user_name} прикусил(-а) губу {reply_user_name} во время страстного поцелуя", parse_mode='html')

    if message.text.lower() == "украсть шапку": 
        user_name = message.from_user.get_mention(as_html=True) 
        reply_user_name = message.reply_to_message.from_user.get_mention(as_html=True) 
        reply = message.reply_to_message 
        if reply: 
            replyuser = reply.from_user 
            await bot.send_message(message.chat.id, f" 🧢 | {user_name} украл(-а) шапку у {reply_user_name}", parse_mode='html') 
    if message.text.lower() == "раздеть": 
        user_name = message.from_user.get_mention(as_html=True) 
        reply_user_name = message.reply_to_message.from_user.get_mention(as_html=True) 
        reply = message.reply_to_message 
        if reply: 
            replyuser = reply.from_user 
            await bot.send_message(message.chat.id, f"🙈 | {user_name} аккуратно раздел(-а) {reply_user_name}", parse_mode='html')

# открытки 
    if message.text.startswith("фото открытки"):
        msg = message
        user_id = msg.from_user.id
        name = message.from_user.get_mention(as_html=True) 
        number = int(msg.text.split()[2])
        num = number + 2
        if number <= 22 and number >= 1:
            cursor.execute(f"UPDATE user SET photo_otkr = '{number}' WHERE id = '{user_id}'")
            await message.reply(f"🌅 | {name}, вы установили <a href='https://t.me/NORM_album/{num}/'>{number}</a>-ю фотографию на фон своей открытки.", parse_mode='html')
        else:
            await message.reply(f"{name}, в данный момент доступно лишь 22 открытки.", parse_mode='html')

    if message.text.startswith("Фото открытки"):
        msg = message
        user_id = msg.from_user.id
        name = message.from_user.get_mention(as_html=True) 
        number = int(msg.text.split()[2])
        num = number + 2
        if number <= 22 and number >= 1:
            cursor.execute(f"UPDATE user SET photo_otkr = '{number}' WHERE id = '{user_id}'")
            await message.reply(f"🌅 | {name}, вы установили <a href='https://t.me/NORM_album/{num}/'>{number}</a>-ю фотографию на фон своей открытки.", parse_mode='html')
        else:
            await message.reply(f"{name}, в данный момент доступно лишь 22 открытки.", parse_mode='html')

# отправка открытки 
    if message.text.startswith("Отправить открытку"):
        msg = message 
        user_id = msg.from_user.id 
        reply_id = msg.reply_to_message.from_user.id
        reply = message.reply_to_message 
        name = message.from_user.get_mention(as_html=True) 
        cursor.execute("SELECT * FROM users WHERE id=?", (reply_id,))
        data = cursor.fetchone()
        text = " ".join(msg.text.split()[2:])
        texts = f"📥 <b>Вам пришла открытка</b>:\n    👤 Отправитель: {name}\n\n 📃 Текст открытки: <code>{text}</code>"
        ph = cursor.execute(f"SELECT photo_otkr FROM user WHERE id = '{user_id}'").fetchone()
        ph = int(ph[0])
        if ph == 1:
            photo = open('otkr/o1.jpg', 'rb')
        if ph == 2:
            photo = open('otkr/o2.jpg', 'rb')
        if ph == 3:
            photo = open('otkr/o3.jpg', 'rb')
        if ph == 4:
            photo = open('otkr/o4.jpg', 'rb')
        if ph == 5:
            photo = open('otkr/o5.jpg', 'rb')
        if ph == 6:
            photo = open('otkr/o6.jpg', 'rb')
        if ph == 7:
            photo = open('otkr/o7.jpg', 'rb')
        if ph == 8:
            photo = open('otkr/o8.jpg', 'rb')
        if ph == 9:
            photo = open('otkr/o9.jpg', 'rb')
        if ph == 10:
            photo = open('otkr/o10.jpg', 'rb')
        if ph == 11:
            photo = open('otkr/o11.jpg', 'rb')
        if ph == 12:
            photo = open('otkr/o12.jpg', 'rb')
        if ph == 13:
            photo = open('otkr/o13.jpg', 'rb')
        if ph == 14:
            photo = open('otkr/o14.jpg', 'rb')
        if ph == 15:
            photo = open('otkr/o15.jpg', 'rb')
        if ph == 16:
            photo = open('otkr/o16.jpg', 'rb')
        if ph == 17:
            photo = open('otkr/o17.jpg', 'rb')
        if ph == 18:
            photo = open('otkr/o18.jpg', 'rb')
        if ph == 19:
            photo = open('otkr/o19.jpg', 'rb')
        if ph == 20:
            photo = open('otkr/o20.jpg', 'rb')
        if ph == 21:
            photo = open('otkr/o21.jpg', 'rb')
        if ph == 22:
            photo = open('otkr/o22.jpg', 'rb')
            
        if reply:
            if data is None:
                await message.reply(f"😖 | {name}, получатель не найден, возможно он не писал мне в ЛС.", parse_mode='html')
            else:
                await bot.send_photo(message.reply_to_message.from_user.id, photo, caption=texts, parse_mode='html')
                await message.reply(f"Открытка отправлена 😃")
        else:
            await message.reply(f"{name}, кому открытка то?", parse_mode='html')
        

# админ команды 
    if message.text.lower() == ".обнулить":
        msg = message
        user_id = msg.from_user.id
        name = msg.from_user.last_name 
        rname =  msg.reply_to_message.from_user.last_name 
        user_name = message.from_user.get_mention(as_html=True)
        reply_user_name = message.reply_to_message.from_user.get_mention(as_html=True)
        reply_user_id = msg.reply_to_message.from_user.id
        st = cursor.execute(f"SELECT status FROM user WHERE id = '{user_id}'").fetchone()
        st = int(st[0])
        if st == 0:
            await message.reply(f"{user_name}, у тебя нет прав ☹️", parse_mode='html')
        elif st >= 2:
            await message.answer(f"😔 | {user_name} обнулил(-а) {reply_user_name}", parse_mode='html')
            cursor.execute(f'UPDATE user SET balance = {0} WHERE id = "{reply_user_id}"')
            connect.commit()    
            

    if message.text.startswith("выдать"):
        msg = message
        user_id = msg.from_user.id
        name = msg.from_user.last_name 
        rname =  msg.reply_to_message.from_user.last_name 
        user_name = message.from_user.get_mention(as_html=True)
        reply_user_name = message.reply_to_message.from_user.get_mention(as_html=True)
        reply_user_id = msg.reply_to_message.from_user.id
        sredsv = int(msg.text.split()[1])
        balance = cursor.execute(f"SELECT balance FROM user WHERE id = '{user_id}'")
        balance = int(balance[0])
        st = cursor.execute(f"SELECT status FROM user WHERE id = '{user_id}'").fetchone()
        st = int(st[0])
        if st == 0:
            await message.reply(f"{user_name}, у тебя нет прав ☹️", parse_mode='html')
        elif st >= 2:
            await message.answer(f"{user_name} выдал(-а) {sredstv}$ игроку: {reply_user_name}", parse_mode='html')
            cursor.execute(f'UPDATE user SET balance = {balance + sredstv} WHERE id = "{reply_user_id}"')
            connect.commit()    

    if message.text.lower() == "назначить админа":
        msg = message
        user_id = msg.from_user.id
        name = msg.from_user.last_name 
        rname =  msg.reply_to_message.from_user.last_name 
        user_name = message.from_user.get_mention(as_html=True)
        reply_user_name = message.reply_to_message.from_user.get_mention(as_html=True)
        reply_user_id = msg.reply_to_message.from_user.id
        st = cursor.execute(f"SELECT status FROM user WHERE id = '{user_id}'").fetchone()
        st = int(st[0])
        if st == 0 and st == 2:
            await message.reply(f"{user_name}, у тебя нет прав ☹️", parse_mode='html')
        elif st >= 3:
            await message.answer(f"☀️ | {user_name} назначил(-а) {reply_user_name} админом", parse_mode='html')
            cursor.execute(f'UPDATE user SET status = {2} WHERE id = "{reply_user_id}"')
            connect.commit()    

    if message.text.lower() == "разжаловать админа":
        msg = message
        user_id = msg.from_user.id
        name = msg.from_user.last_name 
        rname =  msg.reply_to_message.from_user.last_name 
        user_name = message.from_user.get_mention(as_html=True)
        reply_user_name = message.reply_to_message.from_user.get_mention(as_html=True)
        reply_user_id = msg.reply_to_message.from_user.id
        st = cursor.execute(f"SELECT status FROM user WHERE id = '{user_id}'").fetchone()
        st = int(st[0])
        if st == 0 and st == 2:
            await message.reply(f"{user_name}, у тебя нет прав ☹️", parse_mode='html')
        elif st >= 3:
            await message.answer(f"😡 | {user_name} разжаловал(-а) {reply_user_name} с звания админа", parse_mode='html')
            cursor.execute(f'UPDATE user SET status = {0} WHERE id = "{reply_user_id}"')
            connect.commit()    

    if message.text.lower() == "подарить вип":
        msg = message
        user_id = msg.from_user.id
        name = msg.from_user.last_name 
        rname =  msg.reply_to_message.from_user.last_name 
        user_name = message.from_user.get_mention(as_html=True)
        reply_user_name = message.reply_to_message.from_user.get_mention(as_html=True)
        reply_user_id = msg.reply_to_message.from_user.id
        st = cursor.execute(f"SELECT status FROM user WHERE id = '{user_id}'").fetchone()
        st = int(st[0])
        if st == 0 and st == 1:
            await message.reply(f"{user_name}, у тебя нет прав ☹️", parse_mode='html')
        elif st >= 2:
            await message.answer(f"☀️ | {user_name} подарил(-а) {reply_user_name} вип-статус", parse_mode='html')
            cursor.execute(f'UPDATE user SET status = {1} WHERE id = "{reply_user_id}"')
            connect.commit()    

    if message.text.lower() == "забрать вип":
        msg = message
        user_id = msg.from_user.id
        name = msg.from_user.last_name 
        rname =  msg.reply_to_message.from_user.last_name 
        user_name = message.from_user.get_mention(as_html=True)
        reply_user_name = message.reply_to_message.from_user.get_mention(as_html=True)
        reply_user_id = msg.reply_to_message.from_user.id
        st = cursor.execute(f"SELECT status FROM user WHERE id = '{user_id}'").fetchone()
        st = int(st[0])
        if st == 0 and st == 1:
            await message.reply(f"{user_name}, у тебя нет прав ☹️", parse_mode='html')
        elif st >= 2:
            await message.answer(f"😡 | {user_name} забрал(-а) {reply_user_name} вип-статус", parse_mode='html')
            cursor.execute(f'UPDATE user SET status = {0} WHERE id = "{reply_user_id}"')
            connect.commit()    

@dp.callback_query_handler(text='zakaz1')
async def inlinebutton_zakaz(callback: types.CallbackQuery):
    await callback.message.answer(f'''Хочешь такого же бота? 😏

Тогда просто напиши сюда -> @php_aleks.

Начинающий кодер
Дает гарантию ✅
Работает качествено и довольно быстро ✅
Не дорого ✅

Чего ты ждёшь, спеши скорее писать ему 😌 ''')
    

@dp.callback_query_handler(text='helps')
async def inlinebutton_help(callback: types.CallbackQuery):
    help = InlineKeyboardMarkup(row_width=2)
    game = InlineKeyboardButton(text='Игровые 🎰', callback_data='game')
    statuss = InlineKeyboardButton(text='Статусы 💎', callback_data='statuss')
    radio = InlineKeyboardButton(text='Радио 📻', callback_data='radio')
    moder = InlineKeyboardButton(text='Модерация 👮', callback_data='moder')
    rp_command = InlineKeyboardButton(text='Рп - команды 🎭', callback_data='rp_command')
    donat = InlineKeyboardButton(text='Донат 💳', callback_data='donat')
    help.add(game, statuss, radio, moder, rp_command, donat)
    await callback.message.answer(f'''👋 Приветствую, какая помощь тебе интересна?

1⃣ | Игровые 🎰
2⃣ | Статусы 💎
3⃣ | Радио 📻
4⃣ | Модерация 👮
5⃣ | Рп - команды 🎭
6⃣ | Донат 💳''', reply_markup=help, parse_mode='html')

@dp.callback_query_handler(text='clikers')
async def inlinebutton_clikers1(callback: types.CallbackQuery):
    clickers = InlineKeyboardMarkup(row_width=3)
    obmen = InlineKeyboardButton(text='обменик 👾 -> 💰', callback_data='obmen')
    click1 = InlineKeyboardButton(text='Клик 👇🏻', callback_data='click1')
    remove = InlineKeyboardButton(text='Удалить', callback_data='remove')
    clickers.add(obmen, click1, remove)
    await callback.message.answer(f"ты будешь кликать или как?", reply_markup=clickers, parse_mode='html')
@dp.callback_query_handler(text='obmen')
async def inlinebutton_obmen(callback: types.CallbackQuery):
    clicks = cursor.execute("SELECT click FROM user").fetchall() 
    click = round(clicks)
    await callback.message.answer(f"Обменять клики можно с помощью команды: «обменять [число]\n Курс на сегодня 1 клик - 2 монетки.\n У вас кликов -> <b>{click}</b>", parse_mode='html')

@dp.callback_query_handler(text='click1')
async def inlinebutton_click(query: types.CallbackQuery):
    clicks = cursor.execute("SELECT click FROM user").fetchall() 
    clicks = int(clicks)
    cursor.execute(f'UPDATE user SET click = {click + 1} where id = ?', (user_id,))
    connect.commit()
    await query.answer(f"{clicks+1} кликов.", parse_mode='html')
@dp.callback_query_handler(text='remove')
async def inlinebutton_remove(callback: types.CallbackQuery):
    await bot.delete_message(callback_query.message.chat.id, callback_query.message.message_id) 
     
@dp.callback_query_handler(text='game')
async def inlinebutton_game(callback: types.CallbackQuery):
    name = message.from_user.get_mention(as_html=True)
    await callback.message.answer(f'''{name}, игровые команды:

📈 | Трейд [сумма] | ⚠
😱 | Риск! 
🎰 | Казино [сумма] 
🤺 | дуэль [сумма] + [реплай] | ⚠
🏦 | б/Балан/хранилище 
🔃 | дать [сумма] 
🎲 | Куб {1-6} [сумма]
🎳 | боулинг [сумма]
🏀 | баскетбол [сумма]
⚽ | футбол [сумма] 

Удачи в фарме монеток 🔥
<b>P.S</b>: Смайлики указывать не нужно.''', parse_mode='html')
     
@dp.callback_query_handler(text='statuss')
async def inlinebutton_status(callback: types.CallbackQuery):
    await callback.message.answer(f'''ℹ Доступные статусы и помощь для них:

💎 VIP - вип статус: 
   Можно купить как за игровые монетки так и за небольшой донат. | 💎 Вип статус даёт немного преимущества над обычными игроками, а именно: 
 1. Указание в профиле что вы VIP 💎
 2. Командой «!инфа» - смотреть профиля других пользователей.


✏ Свои статусы и возможности вы можете писать в ЛС -> @Chelovechik_nep_loxoy''', parse_mode='html')

@dp.callback_query_handler(text='radio')
async def inlinebutton_radio(callback: types.CallbackQuery):
    await callback.message.answer(f''' В разработке.... ''', parse_mode='html')

@dp.callback_query_handler(text='moder')
async def inlinebutton_moder(callback: types.CallbackQuery):
    await callback.message.answer(f'''👮 Команды модерации: 

👞 | Кик/норм кик - выгнать юзера из чата
❌ | Бан/норм бан - блокировка юзера в чате 
🔇 | Мут [время + параметры (с/s, м/m, ч/h, д/d)] - мутит юзера на указанное время, без указания параметров мутит юзера на 1 час.
🆘 | !репорт - зарепортить сообщение.
📌 | .пин - закрепление сообщения на который был реплай

🤐 | Фильтры сквернословия:
+маты - разрешить сквернословить в чате 
-маты - запретить сквернословить в чате | ⚠ 

⚠ <b>Остальное в разработке</b> ''', parse_mode='html')

@dp.callback_query_handler(text='rp_command')
async def inlinebutton_rp(callback: types.CallbackQuery):
    await callback.message.answer(f''' 👾 Список РП - команд: 
    Чмок 
    Выебать
    Дать пять 
    Извиниться 
    Изнасиловать
    Кусь
    Кастрировать 
    Лизнуть
    Обнять
    Поздравить 
    Поцеловать
    Прижать
    Потрогать 
    Пожать руку
    Прижать 
    Похвалить
    Погладить
    Пнуть
    Послать нахуй
    Расстрелять 
    Ущипнуть 
    Уебать
    Ударить
    Укусить
    Убить
    Шлепнуть 
    Подарить энергетик 
     ''', parse_mode='html')

@dp.callback_query_handler(text='donat')
async def inlinebutton_donat(callback: types.CallbackQuery):
    users = cursor.execute("SELECT id FROM users").fetchall() 
    allusers = len(users) 
    chats = cursor.execute("SELECT id FROM chat").fetchall() 
    allchats = len(chats) 
    await callback.message.answer(f'''🤔 <b>Планируете вложить деньги в развитие проекта?</b>

Ознакомится с прайсом можно ниже:

✉ Рассылка в боте - 50₽ || Рассылка в чатах - ❌

👨‍💻 Сделать команду для вашего чата - от 10₽ 
💰 Покупка монет 1.000.000 - 1₽ 
💎 VIP статус - 8₽ 
🐥 Админ статус - 15₽/месяц - 105₽/навсегда 

Оплата: 
🥝 Киви: <code>NORM2CHELL</code>
💳 Карта: <code>5257 5201 2084 5496</code> 

📊 Статистика бота: 
👤 Юзеров в ЛС: <b>{allusers}</b>
🛖 Чатов: <b>{allchats}</b>

❓ Задать вопрос можно тут -> @Chelovechik_nep_loxoy''', parse_mode='html')


    
@dp.callback_query_handler(text='pochta')
async def inlinebutton_pochta(callback: types.CallbackQuery):
    await callback.message.answer(f''' В разработке.... ''')

@dp.callback_query_handler(text='podp')
async def inlinebutton_ref(callback: types.CallbackQuery):
    await callback.message.answer(f"💗 У владельца ботика так же есть свои каналы и чатики:\n\n 🙊 Чатик: @NORMal_chat\n😊 Канал с открытками: @NORM_album\n\nМожешь вступить или подписаться 🙄", parse_mode='html')

@dp.callback_query_handler(lambda c: c.data == "risk")
async def inlinebutton_risk(callback_query: types.CallbackQuery):
       if callback_query.from_user.id == message.from_user.id:
           balance = cursor.execute(f"SELECT balance FROM user WHERE id = ?",(callback_query.from_user.id,)).fetchone()
           stavka = round(int(balance[0]))
           isx = random.randint(1, 2)
           if isx == 1:
               win = stavka * 2
               cursor.execute(f'UPDATE user SET balance = {win} WHERE id = "{callback_query.from_user.id}"').fetchone()
               connect.commit()
               await callback_query.message.edit_text(f"Вы выиграли ваш баланс х2")
           elif isx == 2:
               lose = 0
               cursor.execute(f'UPDATE user SET balance = {0} WHERE id = "{callback_query.from_user.id}"').fetchone()
               connect.commit()
               await callback_query.message.edit_text("Вы проиграли, ваш баланс теперь 0")
       else:
           await bot.answer_callback_query(callback_query.from_user.id, text="Она тебя съест 🐻", show_alert=True)
        

@dp.callback_query_handler(lambda c: c.data == "remove_risk")
async def inlinebutton_remove_risk(callback_query: types.CallbackQuery):
    await callback_query.message.delete()

@dp.callback_query_handler(lambda c: c.data == "telefon")
async def inlinebutton_tellefon(callback_query: types.CallbackQuery):
    t = datetime.now()
    ho = t.hour
    mi = t.minute
    bank = cursor.execute(f"SELECT bank FROM user WHERE id = ?",(callback_query.from_user.id,)).fetchone()
    bank = round(int(bank[0]))
    bank2 = '{:,}'.format(bank)
    krypto = cursor.execute(f"SELECT krypto FROM user WHERE id = ?",(callback_query.from_user.id,)).fetchone()
    krypto = round(int(krypto[0]))
    krypto2 = '{:,}'.format(krypto)
    if bank >= 999999999999999999999999:
        bank = 999999999999999999999999
        cursor.execute(f"UPDATE user SET bank = {999999999999999999999999} where id = ?",(callback_query.from_user.id,))
        connect.commit()
        bank2 = '{:,}'.format(bank)
    else:
        pass 
    if krypto >= 999999999999999999999999:
        krypto = 999999999999999999999999
        cursor.execute(f"UPDATE user SET krypto = {999999999999999999999999} where id = ?",(callback_query.from_user.id,))
        connect.commit()
        krypto2 = '{:,}'.format(krypto)
    else:
        pass 
    await callback_query.message.edit_text(f"\n   📱 Mobile phone     ⏰{ho}:{mi}\n | \n ├ Имя владельца: {callback_query.from_user.full_name} \n\ \n ├ Номер счёта: {callback_query.from_user.id}\n ├ В банке: {bank2}$\n ├ NORMcoin: {krypto2}\n └––––––––––––––––––––––– ", parse_mode='html')


if __name__ == "__main__":
    executor.start_polling(dp, skip_updates=True)