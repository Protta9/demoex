from fastapi import FastAPI, Body
from fastapi.responses import HTMLResponse
import sqlite3
import random
import urllib.parse

app = FastAPI()

conn = sqlite3.connect('task.db')
cur = conn.cursor()

cur.execute('''
CREATE TABLE IF NOT EXISTS Users (
id INTEGER,
date TEXT,
ogrteh TEXT,
model TEXT,
problem TEXT,
phonenumber TEXT,
fio TEXT,
status TEXT,
fixik TEXT,
comm TEXT)
''')

conn.commit()
conn.close()

def add_data(data):
    conn = sqlite3.connect('task.db')
    cur = conn.cursor()
    random_id = str(random.randint(1, 9999999))
    cur.execute('INSERT INTO Users (id, date, ogrteh, model, problem, fio, phonenumber, status, fixik, comm) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)', (random_id, data[0][1], data[1][1], data[2][1], data[3][1], data[4][1], data[5][1], 'Ожидание', 'Не указан', ''))
    conn.commit()
    conn.close()
    return random_id
 
def update_data(data):
    conn = sqlite3.connect('task.db')
    cur = conn.cursor()
    if data[1][1] == 'wait':
        cur.execute('UPDATE Users SET status = ?, problem = ?, fixik = ? WHERE id = ?', ('Ожидание', data[2][1], data[3][1], data[0][1]))
    elif data[1][1] == 'in_process':
        cur.execute('UPDATE Users SET status = ?, problem = ?, fixik = ? WHERE id = ?', ('В процессе', data[2][1], data[3][1], data[0][1]))
    elif data[1][1] == 'ready':
        cur.execute('UPDATE Users SET status = ?, problem = ?, fixik = ? WHERE id = ?', ('Готово', data[2][1], data[3][1], data[0][1]))
    conn.commit()
    conn.close()

def all_list_data():
    conn = sqlite3.connect('task.db')
    cur = conn.cursor()
    cur.execute(f'SELECT * FROM Users')
    result = cur.fetchall()
    conn.close()
    return result

def list_data(data):
    conn = sqlite3.connect('task.db')
    cur = conn.cursor()
    cur.execute(f'SELECT * FROM Users WHERE {data[0][1]} = ?', (data[1][1], ))
    result = cur.fetchall()
    conn.close()
    return result

def stats():
    conn = sqlite3.connect('task.db')
    cur = conn.cursor()
    cur.execute(f'SELECT * FROM Users WHERE status = ?', ('ready'))
    ready_task = len(cur.fetchall())
    return ready_task


@app.get("/index")
def index():
    html_content = '''
    <form action="/add"><button>Добавить</button></form>
    <form action="/update"><button>Редактировать</button></form>
    <form action="/list "><button>Список заявок</button></form>
'''
    return HTMLResponse(content=html_content)

@app.get('/add')
def add():
    html_content='''
    <form action="/index"><button>Обратно</button></form>
    <form action='/apiadd', method=post>
    <label for="Date">Дата заявки</label>
    <input type="text" name="Date" id="Date"/><br>
    <label for="ogrteh">Вид оргтехники</label>
    <input type="text" name="ogrteh" id="ogrteh"/><br>
    <label for="model">Модель</label>
    <input type="text" name="model" id="model"/><br>
    <label for="problem">Проблема</label>
    <input type="text" name="problem" id="problem"/><br>
    <label for="pn">Номер телефона</label>
    <input type="text" name="pn" id="pn"/><br>
    <label for="fio">ФИО</label>
    <input type="text" name="fio" id="fio"/><br>
    <button>add</button>
    </form>
'''
    return HTMLResponse(content=html_content)

@app.post('/apiadd')
def apiadd(data = Body()):
    data = str(data)[2:len(str(data))-1].split('&')
    for i in range(len(data)):
        data[i] = data[i].split('=')
    for i in data:
        for b in range(len(i)):
            i[b] = urllib.parse.unquote(i[b])
    id = add_data(data)
    return HTMLResponse(content=f'<form action="/index""><button>Обратно</button></form><br>Ok<br>Ваш id - {id}')

@app.get('/update')
def update():
    html_content='''
    <form action="/index"><button>Обратно</button></form>
    <form action='/apiupdate', method=post>
    <label for="id">ID заявки</label>
    <input type="text" name="id" id="id"/><br>
    <label for="find">Способ поиска заявки:</label>
    <select id="find" name="find">
    <option value="wait">Ожидание</option>
    <option value="in_process">В процессе</option>
    <option value="ready">Готово</option>
    </select><br>
    <label for="problem">Проблема</label>
    <input type="text" name="problem" id="problem"/><br>
    <label for="h">ответственный за выполнение работ</label>
    <input type="text" name="h" id="h"/><br>
    <button>Подтвердить</button>
    </form>
'''
    return HTMLResponse(content=html_content)

@app.post('/apiupdate')
def apiupate(data = Body()):
    data = str(data)[2:len(str(data))-1].split('&')
    for i in range(len(data)):
        data[i] = data[i].split('=')
    for i in data:
        for b in range(len(i)):
            i[b] = urllib.parse.unquote(i[b])
    update_data(data)
    return HTMLResponse(content='<form action="/index""><button>Обратно</button></form><br>Ok')

@app.get('/list')
def list():
    html_content = '''
    <form action="/index"><button>Обратно</button></form>
    <form action='/apilist', method=post>
    <label for="find">Способ поиска заявки:</label>
    <select id="find" name="find">
    <option value="all">Все</option>
    <option value="id">ID</option>
    <option value="date">Дата</option>
    <option value="ogrteh">Вид оргтехники</option>
    <option value="model">Модель</option>
    <option value="problem">Проблема</option>
    <option value="phonenumber">Номер телефона</option>
    <option value="fio">ФИО</option>
    <option value="status">Статус</option>
    <option value="fixik">Ответственный за выполнение</option>
    </select><br>
    <label for="text">Ввод:</label>
    <input type="text" name="text" id="text"/><br>
    <button>Найти</button>
    </form>
'''
    return HTMLResponse(content=html_content)

@app.post('/apilist')
def apilist(data = Body()):
    data = str(data)[2:len(str(data))-1].split('&')
    for i in range(len(data)):
        data[i] = data[i].split('=')
    for i in data:
        for b in range(len(i)):
            i[b] = urllib.parse.unquote(i[b])

    if data[0][1] == 'all':
        result = all_list_data()
        html_content = '<form action="/index"><button>Обратно</button></form><br><br>'
        for i in result:
            html_content = html_content + f'<br>        |       {i[0]}        |       {i[1]}        |       {i[2]}        |       {i[3]}        |       {i[4]}        |       {i[5]}        |       {i[6]}        |       {i[7]}        |       {i[8]}'
        return HTMLResponse(content=html_content)

    result = list_data(data)
    html_content = '<form action="/index"><button>Обратно</button></form><br><br>'
    for i in result:
        html_content = html_content + f'<br>        |       {i[0]}        |       {i[1]}        |       {i[2]}        |       {i[3]}        |       {i[4]}        |       {i[5]}        |       {i[6]}        |       {i[7]}        |       {i[8]}'
    return HTMLResponse(content=html_content)

@app.get('/stats')
def stats():
    html_content = f'''
<p>Статистика</p><br>
Количество выполненных заявок: {stats()}
'''
    return HTMLResponse(content=html_content)