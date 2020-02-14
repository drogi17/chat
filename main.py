from flask import Flask, request, render_template, jsonify, send_from_directory, redirect, make_response
from flask_socketio import SocketIO, send #библиотека
from modules.sqlite_inquiries import DataBase
import os, sys
import json
from emojis.emoji import amoji_dict
from modules.user import avatar


def get_link_in_str(string):
    for all_words in string.split(' '):
        if '.' in all_words:
            if 'https://' in string:
                string = string.replace(all_words, '<a href="' + all_words + '" target="_blank">' + all_words.replace('https://', '') + '</a>')
            elif 'http://' in string:
                string = string.replace(all_words, '<a href="' + all_words + '" target="_blank">' + all_words.replace('http://', '') + '</a>')
    return string

db = DataBase('data/data.db')
app = Flask(__name__)
app.config['SECRET_KEY'] = 'mysecret'
socketio = SocketIO(app)
command_list = {
    '?clear': db.delete,
}

@app.route('/', methods=['GET'])
def index():
    where = ['name = "' + str(request.cookies.get('username')).replace("'", '"') + '"']
    id_usr = db.simple_select('users', 'id', where)
    print(request.cookies.get('username'))
    if request.cookies.get('username') and request.cookies.get('username') != '' and id_usr:
        return render_template('index.html')
    else:
        return render_template('login.html')

@app.route('/login', methods=['POST'])
def login():
    name = str(request.data.decode('utf-8')).replace("'", '"').replace('<', '&lt;').replace('>', '&gt;')
    if name == 'SERVER':
        return ''
    where = ['name = "' + str(name) + '"']
    data = db.simple_select('users', '*', where)
    if not data:
        data = { 'name': name, 'avatar': avatar(name)}
        db.insert('users', data)  
    data_inc = {'user_id': 0, 'message': '[' + name + '] JOINED'}
    db.insert('messages', data_inc)
    resp = make_response({})
    resp.set_cookie('username', name)
    return resp


@socketio.on('message')
def handleMessage(msg):
    msg = msg['data']
    data = str(msg).replace("'", '"').replace('<', '&lt;').replace('>', '&gt;')
    if len(data) > 1000:
        data = data[:1000]
    data = get_link_in_str(data)
    for emoj in amoji_dict:
        if emoj in data:
            data = data.replace(emoj, '<img src="' + amoji_dict[emoj] + '" title="' + emoj + '" class="emoji-img">')
    adr = str(request.cookies.get('username'))
    where = ['name = "' + str(adr) + '"']
    try:
        id_usr = db.simple_select('users', 'id', where)[0][0]
        if data != "" and id_usr:
            data_inc = {'user_id': id_usr, 'message': data}
            db.insert('messages', data_inc)
        if data in command_list:
            command = command_list.get(data)
            command('messages', '')
        elif data == '?exit' or request.cookies.get('username') == '':
            data_inc = {'user_id': 0, 'message': '[' + str(adr) + '] LEFT'}
            db.insert('messages', data_inc)
            send('exit')
        data_to_send = db.custom_request("""    SELECT users.name, users.avatar, messages.message
                                                FROM messages 
                                                INNER JOIN users ON messages.user_id = users.id;""")
        send(data_to_send, broadcast=True)
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