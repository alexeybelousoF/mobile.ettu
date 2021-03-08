import os
import psycopg2

DATABASE_URL = os.environ['DATABASE_URL']

print("Database opened successfully")

def set_saved(chat_id, url, station_name):
  con = bd_init()
  cur = con.cursor()
  try:
    print(cur)
    cur.execute(
      "INSERT INTO userdata (chat_id,url,station_name) VALUES ('" + chat_id +
      "', '" + url + "', '" + station_name + "')"
    )
    print('Сохранение для юзера '+ chat_id + ' Страничка ' + url)
    con.commit()
    con.close()

  except saveError as err:
    print(err)

def get_saved(chat_id):
  con = bd_init()
  cur = con.cursor()
  cur.execute(
    "SELECT ALL url,station_name FROM userdata where chat_id = '"+chat_id+"'"
  )
  res = cur.fetchall()
  con.close()
  return res

def bd_init():
  con = psycopg2.connect(DATABASE_URL, sslmode='require')
  return con

def create_table_once():
  con = bd_init()
  cur = con.cursor()
  try:
    cur.execute('''CREATE TABLE userdata 
       (id SERIAL,
       chat_id CHAR(25) NOT NULL,
       url TEXT UNIQUE NOT NULL, 
       station_name TEXT NOT NULL);''')
    print("Table created successfully")
    print(cur)
    
  except creaeTableError as err:
    print(err)
    
    
create_table_once()
