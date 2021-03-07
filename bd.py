import psycopg2
# DATABASE_URL = os.environ['DATABASE_URL']

print("Database opened successfully")

cur.execute('''CREATE TABLE userdata 
     (id SERIAL,
     CHAT_ID CHAR(25) NOT NULL,
     URL TEXT UNIQUE NOT NULL, station_name TEXT NOT NULL);''')
print("Table created successfully")

def set_saved(chat_id, url, station_name):
  con = bd_init()
  cur = con.cursor()
  cur.execute(
    "INSERT INTO userdata (CHAT_ID,URL,station_name) VALUES ('"+ chat_id +"', '"+ url + "', '"+ station_name + "')"
  )
  print('Сохранение для юзера '+ chat_id + ' Страничка ' + url)
  con.commit()
  con.close()

def get_saved(chat_id):
  con = bd_init()
  cur = con.cursor()
  cur.execute(
    "SELECT ALL URL,station_name FROM userdata where CHAT_ID = '"+chat_id+"'"
  )
  res = cur.fetchall()
  con.close()
  return res

def bd_init():
  con = psycopg2.connect(DATABASE_URL, sslmode='require')
  return con
