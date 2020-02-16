from flask import Flask, request, render_template, jsonify, send_from_directory, redirect, make_response
from flask_socketio import SocketIO, send #библиотека
from modules.sql_request import DataBase
import os, sys
import json
from emojis.emoji import amoji_dict
from modules.user import avatar


def get_link_in_str(string):                        # Определение ссылок
    for all_words in string.split(' '):
        if '.' in all_words:
            if 'https://' in string:
                string = string.replace(all_words, '<a href="' + all_words + '" target="_blank">' + all_words.replace('https://', '') + '</a>')
            elif 'http://' in string:
                string = string.replace(all_words, '<a href="' + all_words + '" target="_blank">' + all_words.replace('http://', '') + '</a>')
    return string


db = DataBase('data/data.db')   #Подключение к бд
app = Flask(__name__)           #Запуск flask
app.config['SECRET_KEY'] = 'mysecret'
socketio = SocketIO(app)        #Запуск socketio


@app.route('/', methods=['GET'])# начальная дерриктория
def index():
    usr_status = db.request("""SELECT status
                            FROM users
                            WHERE name = '%s';""", (str(request.cookies.get('username'))))
    print(usr_status)
    if request.cookies.get('username') and request.cookies.get('username') != '' and usr_status and usr_status[0][0] == 'online':
        return render_template('index.html')
    else:
        return render_template('login.html')

@app.route('/chats/<chat>', methods=['GET'])# Страница чата - Идентична начальной дериктории
def chats(chat):
    usr_status = db.request("""SELECT status
                            FROM users
                            WHERE name = '%s';""", (str(request.cookies.get('username'))))
    if request.cookies.get('username') and request.cookies.get('username') != '' and usr_status and usr_status[0][0] == 'online':
        return render_template('index.html')
    else:
        return redirect('/')

@app.route('/add_chat/<chat>')#Добавить Чат
def add_chat(chat):
    chat = chat.replace(' ', '%20')             ### КОНЧЕНЫЕ ДЕЙСТВИЯ
    avatar_chat = request.args.get('avatar')# получение аватарки
    if not avatar_chat:                     # Если ее нет, то заменить на дфолтную
        avatar_chat = 'https://s1.iconbird.com/ico/2013/9/446/w512h5121380376442MetroUIMessagingAlt.png'
    alredy_created = db.request("""SELECT id                    
                            FROM chats                          
                            WHERE name = '%s';""", (str(chat))) # Существует ли чат
    if not alredy_created:
        db.request("""INSERT INTO chats (name, avatar)                                  
                            VALUES ('%s', '%s');""", (str(chat), str(avatar_chat)))     # Записать чат
    return redirect('/')



@app.route('/get_chats', methods=['GET'])# Вывод всех чатов
def get_chats():
    data = db.request("""SELECT name, avatar
                            FROM chats;""")
    return {'text':data}


@app.route('/login', methods=['POST'])# Регистрация пользователей
def login():
    name = str(request.data.decode('utf-8')).replace('<', '&lt;').replace('>', '&gt;')# получение данных с формы регистрации
    if name == 'SERVER' or name == '': 
        return ''
    data = db.request("""SELECT id                          
                            FROM users                      
                            WHERE name = '%s';""", (name))  # есть ли юзер в базе 
    if not data:
        db.request("""INSERT INTO users (name, avatar)                  
                        VALUES ('%s', '%s');""", (name, avatar(name)))  # Занесение в базу
    db.request("""  UPDATE users
                        SET status = 'online'
                        WHERE name = '%s';""", (name))
    # data_inc = {'user_id': 0, 'message': '[' + name + '] JOINED'}
    # db.insert('messages', data_inc)
    resp = make_response({})            ### ОЧЕНЬ ХЕРОВАЯ СИСТЕМА ### ДОБАВЛЕНИЕ КУКИСОВ
    resp.set_cookie('username', name)   ### ОЧЕНЬ ХЕРОВАЯ СИСТЕМА ### ДОБАВЛЕНИЕ КУКИСОВ
    return resp


@socketio.on('message') # Сообщения
def handleMessage(msg):
    if msg == '$exit$':
        db.request("""  UPDATE users
                        SET status = 'offline'
                        WHERE name = '%s';""", (str(request.cookies.get('username'))))
        send('exit')
    chat = msg.get('chat').replace('%20', ' ')                                  ###
    msg = msg.get('data')                                                       ### КОНЧЕНЫЕ ДЕЙСТВИЯ
    data = str(msg).replace('<', '&lt;').replace('>', '&gt;') ###
    adr = str(request.cookies.get('username'))
    if len(data) > 1000:            # Проверка на размер сообщения
        data = data[:1000]
    data = get_link_in_str(data)    # Наличие ссылок
    for emoj in amoji_dict:         # Наличие эмоджи
        if emoj in data:
            data = data.replace(emoj, '<img src="' + amoji_dict[emoj] + '" title="' + emoj + '" class="emoji-img">')
    try:
        id_usr = db.request("""SELECT id                                
                            FROM users                                  
                            WHERE name = '%s';""", (str(adr)))[0][0]    # Получение id юзера. Да, знаю. Можно вынести в общий запрос. Но мне так удобнее
        id_chat = db.request("""SELECT id                               
                            FROM chats                                  
                            WHERE name = '%s';""", (str(chat)))         # Чат, в который он пишет. Да, знаю. Можно вынести в общий запрос. Но мне так удобнее
        if data != "" and id_usr and id_chat: # если сообщение номальное, юзер регнутый и чат существует
            db.request("""INSERT INTO messages (id_user, id_chat, message)                          
                        VALUES (%s, %s, '%s');""", (str(id_usr), str(id_chat[0][0]), str(data)))    # Внести сообщение в базу
        if data == '?clear' and id_chat:      # очистить чат 
            db.request("""DELETE
                        FROM messages
                        WHERE messages.id_chat = (SELECT chats.id
                                                    FROM chats
                                                    WHERE chats.name = '%s');""", (chat))
            # db.request("""DELETE
            #             FROM messages
            #             INNER JOIN chats ON messages.id_chat = chats.id
            #             WHERE chats.name = '%s';""", (chat))
        # elif data == '?exit' or request.cookies.get('username') == '': #выйти из системы. Реализовано через жопу. Заменить макс. быстро
        #     db.request("""INSERT INTO messages (id_user, id_chat, message)
        #                 VALUES (%s, %s, '%s');""", (str(0), str(id_chat[0][0]), '[' + str(adr) + '] LEFT'))
        #     send('exit')
        data_to_send = db.request("""    SELECT users.name, users.avatar, messages.message, chats.name   
                                                FROM messages                                           
                                                INNER JOIN users ON messages.id_user = users.id         
                                                INNER JOIN chats ON messages.id_chat = chats.id;""")    # Получить все сообщения.
                                                # WHERE chats.name = '%s';""", (str(chat)))
        send(data_to_send, broadcast=True) # отправка ВСЕМ ВСЕХ СООБЩЕНИЙ
    except IndexError:
        send('exit')

port = 5000
host = '127.0.0.1'
if '--host' in sys.argv:
    nomb = sys.argv.index('--host') + 1
    try:
        host=sys.argv[nomb]
    except IndexError:
        pass

if '--port' in sys.argv:
    nomb = sys.argv.index('--port') + 1
    try:
        port = int(sys.argv[nomb])
    except:
        pass

if __name__ == "__main__":
	app.run(debug=True, host=host, port=port)