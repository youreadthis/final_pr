import sqlite3
from config import (BD_NAME,MAX_GPT_TOKENS,MAX_TTS_TOKEN,MAX_STT_BLOCK, MAX_USERS)
def reqwest_bd(sql_query, values=None):
    connection = sqlite3.connect(f'{BD_NAME}.db')
    cursor = connection.cursor()
    if values:
        cursor.execute(sql_query, values)
    else:
        cursor.execute(sql_query)

    connection.commit()
    connection.close()

def get_reqwest(sql_query, values = None,):
    connection = sqlite3.connect(f'{BD_NAME}.db')
    cursor = connection.cursor()
    if values:
        cursor.execute(sql_query, values)
    else:
        cursor.execute(sql_query)
    rows = cursor.fetchone()
    connection.close()
    return rows

def create_table():
    con = sqlite3.connect(f'{BD_NAME}.db')
    cur = con.cursor()
    query = f'''
        CREATE TABLE IF NOT EXISTS gpt(
            id INTEGER PRIMARY KEY,
            User_id TEXT,
            Token INTEGER
        );
        '''
    cur.execute(query)
    query = f'''
            CREATE TABLE IF NOT EXISTS tts(
                id INTEGER PRIMARY KEY,
                User_id TEXT,
                Token INTEGER
            );
            '''
    cur.execute(query)
    query = f'''
                CREATE TABLE IF NOT EXISTS stt(
                    id INTEGER PRIMARY KEY,
                    User_id TEXT,
                    Blok INTEGER
                );
                '''
    cur.execute(query)
    con.close()

def create_user(user_id):
    if count_users():
        seve_in_bd_TTS(user_id,0)
        seve_in_bd_STT(user_id,0)
        seve_in_bd_GPT(user_id, 0)
    else:
        return False

def check_user(user_id):
    if select_user_last_TTS_TOK(user_id) and select_user_last_STT_Blok(user_id) and select_user_last_GPT_TOK(user_id) and count_users():

        return True
    else:
        return False

def count_users(max_users = MAX_USERS):
    connection = sqlite3.connect(f'{BD_NAME}.db')
    cursor = connection.cursor()
    result = cursor.execute('SELECT DISTINCT User_id FROM gpt;')
    count = 0 # количество пользователей
    for i in result: # считаем количество полученных строк
        count += 1 # одна строка == один пользователь
    connection.close()
    return count <= max_users

def user_check_all(user_id):
    if user_check_TTS(user_id) and user_check_STT(user_id) and user_check_GPT(user_id):
        return True
    else:
        return False

#TTS
def seve_in_bd_TTS(user_id,tokens):
    reqwest = f'''INSERT INTO tts (User_id, Token)
    VALUES (?, ?);'''
    reqwest_bd(reqwest, (user_id,  tokens + select_user_last_TTS_TOK(user_id)))
def select_user_last_TTS_TOK(user_id):
    sql_query = f"SELECT Token FROM tts WHERE User_id = ? ORDER BY id DESC LIMIT 1;"
    answ = get_reqwest(sql_query, (user_id,))
    if answ:
        return answ[0]
    else:
        return False

def user_check_TTS(user_id):
    if MAX_TTS_TOKEN > select_user_last_TTS_TOK(user_id):
        return True
    else:
        return False

#STT
def select_user_last_STT_Blok(user_id):
    sql_query = f"SELECT Blok FROM stt WHERE User_id = ? ORDER BY id DESC LIMIT 1;"
    answ = get_reqwest(sql_query,(user_id,))
    if answ:
        return answ[0]
    else:
        return  False
def seve_in_bd_STT(user_id,bloks):
    reqwest = f'''INSERT INTO stt (User_id, Blok)
    VALUES (?, ?);'''
    reqwest_bd(reqwest, (user_id, bloks + select_user_last_STT_Blok(user_id)))

def user_check_STT(user_id):
    if MAX_STT_BLOCK > select_user_last_STT_Blok(user_id):
        return True
    else:
        return False

#GPT
def select_user_last_GPT_TOK(user_id):
    sql_query = f"SELECT Token FROM gpt WHERE User_id = ? ORDER BY id DESC LIMIT 1;"
    answ = get_reqwest(sql_query,(user_id,))
    if answ:
        return answ[0]
    else:
        return  False
def seve_in_bd_GPT(user_id,tokens):
    reqwest = f'''INSERT INTO gpt (User_id, Token)
       VALUES (?, ?);'''
    reqwest_bd(reqwest, (user_id, tokens + select_user_last_GPT_TOK(user_id)))

def user_check_GPT(user_id):
    if MAX_GPT_TOKENS > select_user_last_GPT_TOK(user_id):
        return True
    else:
        return False