from flask import Flask, request, render_template, jsonify, send_from_directory, redirect, make_response
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
command_list = {
    '?clear': db.delete,
}

@app.route('/', methods=['GET'])
def index():
    if request.cookies.get('username') and request.cookies.get('username') != '':
        return render_template('index.html')
    else:
        return render_template('login.html')

@app.route('/login', methods=['POST'])
def login():
    name = str(request.data.decode('utf-8')).replace("'", '"').replace('<', '&lt;').replace('>', '&gt;')
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


@app.route('/send_text', methods=['POST'])
def send_text():
    data = str(request.data.decode('utf-8')).replace("'", '"').replace('<', '&lt;').replace('>', '&gt;')
    if len(data) > 1000:
        data = data[:1000]
    data = get_link_in_str(data)
    for emoj in amoji_dict:
        if emoj in data:
            data = data.replace(emoj, '<img src="' + amoji_dict[emoj] + '" title="' + emoj + '" class="emoji-img">')
    adr = str(request.cookies.get('username'))
    if adr == '':
        return {'exit': 1}
    where = ['name = "' + str(adr) + '"']
    try:
        id_usr = db.simple_select('users', 'id', where)[0][0]
        if data != "":
            data_inc = {'user_id': id_usr, 'message': data}
            db.insert('messages', data_inc)
        if data in command_list:
            command = command_list.get(data)
            command('messages', '')
        elif data == '?exit' or not id_usr:
            resp = make_response({'exit': 1})
            resp.set_cookie('username', '')
            data_inc = {'user_id': 0, 'message': '[' + str(adr) + '] LEFT'}
            db.insert('messages', data_inc)
            return resp
    except IndexError:
        resp = make_response({'exit': 1})
        resp.set_cookie('username', '')
        return resp
    return {'exit': 0}

@app.route('/get_messages', methods=['GET'])
def get_messages():
    data_to_send = db.custom_request("""   SELECT users.name, users.avatar, messages.message
                            FROM messages 
                            INNER JOIN users ON messages.user_id = users.id;""")
    return {'text':data_to_send}

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