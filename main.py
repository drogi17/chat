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
            # else:
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
        data = { 'name': name, 'avatar': avatar(300, name)}
        db.insert('users', data)
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
    print(adr)
    if adr == '':
        return {'exit': 1}
    where = ['name = "' + str(adr) + '"']
    # id_usr = db.simple_select('users', 'id', where)
    # if not id_usr:
    #     dat = { 'name': adr}
    #     db.insert('users', dat)
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
            # resp = make_response(render_template('index.html'))
            resp.set_cookie('username', '')
            return resp
    except IndexError:
        resp = make_response({'exit': 1})
        # resp = make_response(render_template('index.html'))
        resp.set_cookie('username', '')
        return resp
    return {'exit': 0}

# @app.route('/get_messages', methods=['GET'])
# def get_messages():
#     data_to_send = db.custom_request("""   SELECT users.name, messages.message
#                             FROM messages 
#                             INNER JOIN users ON messages.user_id = users.id;""")
#     send_str = ''
#     for data_mess in data_to_send:
#         send_str += '[' + data_mess[0] + ']: ' + data_mess[1] + '<br>'
#     return {'data':send_str}

@app.route('/get_messages', methods=['GET'])
def get_messages():
    data_to_send = db.custom_request("""   SELECT users.name, users.avatar, messages.message
                            FROM messages 
                            INNER JOIN users ON messages.user_id = users.id;""")
    # send_list = []
    # for data_mess in data_to_send:
    #     send_list.append(data_mess)
    return {'text':data_to_send}
