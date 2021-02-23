# -*- coding: utf-8 -*-
import telebot;
from parser_app import *
from telebot import types
bot = telebot.TeleBot('1432032022:AAEqosR1uqUnFVhAuqc617YaGq45nBEiDy8');

@bot.message_handler(content_types=['text'])
def start_app(message):
    keyboard = types.InlineKeyboardMarkup(); #наша клавиатура
    tram_app = types.InlineKeyboardButton(text='Где трамвай', callback_data='tram');
    keyboard.add(tram_app)
    saved = types.InlineKeyboardButton(text='Сохраненные', callback_data='saved');
    keyboard.add(saved)
    bot.send_message(message.from_user.id, text="Читай меню", reply_markup=keyboard)


@bot.callback_query_handler(func=lambda call: True)
def first_screen(call):
  if call.data.startswith('/stations/'):
    tram_stations(call.message.chat.id, call.data)
  elif call.data.startswith('/station/'):
    schedule(call.message.chat.id, call.data)
  elif call.data == "tram":
      tram_main(call.message.chat.id)
  elif call.data == "saved":
      bot.send_message(call.message.chat.id, 'Показываем сохраненки : )');

def tram_main(chat_id):
  links = get_main()
  keyboard = types.InlineKeyboardMarkup();
  for item in links:
    button = types.InlineKeyboardButton(item.text, callback_data=item.get('href'));
    keyboard.add(button)

  bot.send_message(chat_id, text="Первая буква остановки :", reply_markup=keyboard)

def tram_stations(chat_id, url):
  keyboard = types.InlineKeyboardMarkup();
  title = ''
  links = get_stations(url)
  bot.send_message(chat_id, 'Выбери остановку :');
  for item in links:
    if item.name == 'a':
      button = types.InlineKeyboardButton(item.text, callback_data=item.get('href'));
      keyboard.add(button)
    else:
      if (keyboard and title):
        bot.send_message(chat_id, title, reply_markup=keyboard)
      title = item.text + ' : '
      keyboard = types.InlineKeyboardMarkup();

  bot.send_message(chat_id, title, reply_markup=keyboard)

def schedule(chat_id, url):
  items = get_schedule(url)
  i = 0
  number = ''
  time = ''
  distance = ''
  for item in items:
      bot.send_message(chat_id, item.text);
  
  keyboard = types.InlineKeyboardMarkup();
  button = types.InlineKeyboardButton("Обновить", callback_data=url);
  keyboard.add(button)
  bot.send_message(chat_id, 'Пока все', reply_markup=keyboard)
  

bot.polling(none_stop=True, interval=0)