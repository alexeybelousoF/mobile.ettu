# -*- coding: utf-8 -*-
import requests
from bs4 import BeautifulSoup
TRAM_URL = 'https://mobile.ettu.ru/'

def get_main():
  responce = requests.get(TRAM_URL)
  html = BeautifulSoup(responce.text, "lxml")
  links = html.find_all('a', {'class': 'letter-link'}) #все ссылки
  return links

def get_stations(url):
  responce = requests.get(TRAM_URL + url)
  html = BeautifulSoup(responce.text, "lxml")
  tram = html.find('h3') #Трамваи trolleybus
  stations = [] # Сборщик станций + названий
  stations.append(tram)
  item = tram

  while item.name != 'p':
    item = item.next_element
    if (item.name and item.name != 'br'):
      stations.append(item)

  del stations[-1]
  return stations

def get_schedule(url):
  responce = requests.get(TRAM_URL + url)
  html = BeautifulSoup(responce.text, "lxml")
  header = html.find('p') #Первый п на странице - От него начинаем
  schedule = [] # Сборщик времени + номеров
  schedule.append(header)
  item = header
  while item.name != 'script':
    item = item.next_sibling
    if not item:
      break
    elif (item.name and item.name == 'div'):
      schedule.append(item)

  if len(schedule) == 1 :
    return schedule

  del schedule[-1]
  return schedule
