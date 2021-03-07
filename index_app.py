# -*- coding: utf-8 -*-
import os
from flask import Flask, request
import telebot;
from parser_app import *
from bd import *
from telebot import types

# TG_TOKEN = '<api_token>' #токен под хероку
bot = telebot.TeleBot(TG_TOKEN);
server = Flask(__name__)

@bot.message_handler(content_types=['text'])
def start_app(message):
    if len(message.text) == 1:
      tram_main(message)
    else:
      keyboard = types.InlineKeyboardMarkup(); #наша клавиатура
      saved = types.InlineKeyboardButton(text='Сохраненные', callback_data='saved');
      keyboard.add(saved)
      bot.send_message(message.from_user.id, text="Напиши первую букву улицы", reply_markup=keyboard)

@bot.callback_query_handler(func=lambda call: True)
def first_screen(call):
  if call.data.startswith('add_to_save'):
    data = call.data.replace('add_to_save','')
    station_name = get_schedule(data)[0].text.partition(',')[0]
    chat_id = str(call.message.chat.id)
    set_saved(chat_id, data, station_name.strip())
  elif call.data.startswith('/stations/'):
    tram_stations(call.message.chat.id, call.data)
  elif call.data.startswith('/station/'):
    print(call.data)
    schedule(call.message.chat.id, call.data)
  elif call.data == "saved":
    chat_id = str(call.message.chat.id)
    saved = get_saved(chat_id)
    keyboard = types.InlineKeyboardMarkup();
    for item in saved:
      print(item[0])
      print(item[1])
      button = types.InlineKeyboardButton(str(item[1]), callback_data=str(item[0]));
      keyboard.add(button)

    bot.send_message(call.message.chat.id, "Сохраненные остановки:", reply_markup=keyboard)

def tram_main(message):
  links = get_main()
  for item in links:
    if item.text == message.text:
      tram_stations(message.chat.id, item.get('href'))
      return


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
  all_text = ''
  item_name = ''
  check_first = True
  for item in items:
    if check_first:
      check_first = False
      all_text += item.text
      if len(items):
        all_text += "Нет данных"
    else:
      all_text += '____🚈____' + item.text

  bot.send_message(chat_id, all_text);
  keyboard = types.InlineKeyboardMarkup();
  button = types.InlineKeyboardButton("Обновить", callback_data=url);
  save = types.InlineKeyboardButton("Сохранить", callback_data='add_to_save'+url);
  keyboard.row(button, save)
  bot.send_message(chat_id, 'Чтобы перейти в меню, напишите 2 буквы или больше', reply_markup=keyboard)
  

@server.route('/', methods=['POST']) #+ TOKEN
def getMessage():
    bot.process_new_updates([telebot.types.Update.de_json(request.stream.read().decode("utf-8"))])
    return "!", 200


@server.route("/")
def webhook():
    bot.remove_webhook()
    bot.set_webhook(url='https://ettu-app.herokuapp.com/') #+ TOKEN
    return "!", 200


server.run(host="0.0.0.0", port=int(os.environ.get('PORT', 33507)))