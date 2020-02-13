import sqlite3


class DataBase:
    def __init__(self, data_base_file):
        self.conn = sqlite3.connect(data_base_file, check_same_thread=False)
        self.cursor = self.conn.cursor()

    def custom_request(self, request):
        request_data = self.cursor.execute(request).fetchall()
        self.conn.commit()
        return request_data

    def simple_select(self, table, columns, arguments=None):    # Таблица(str), колонки(str/list), аргуменыт(str/list/None)
        columns_t   = type(columns).__name__
        arguments_t = type(arguments).__name__
        request = 'SELECT '
        if columns_t == 'list':
            for column in columns:
                request += str(column) + ','
            request = request[:(len(request) - 1)] + '\n'
        elif columns_t == 'str':
                request += str(columns) + '\n'
        request += 'FROM ' + str(table)
        if arguments and arguments != '':
            request += '\nWHERE '
            if arguments_t == 'list':
                for argument in arguments:
                    request += argument + ' AND '
                request = request[:(len(request) - 4)]
            if arguments_t == 'str':
                request += arguments
        request += ';'
        received_data = self.cursor.execute(request).fetchall()
        return received_data

    def insert(self, table, data):                  # Таблица(str), данные для ввода(dict): {'имя слобца': 'данные'}
        request = 'INSERT INTO ' + str(table) + ' ('
        for column in data:
            request += str(column) + ','
        request = request[:(len(request) - 1)] + ')\n'
        request += 'VALUES ( '
        for data_val in data:
            data_type = type(data[data_val]).__name__
            if data_type == 'str':
                request += "'%s'," % (data[data_val])
            else:
                request += str(data[data_val]) + ","
        request = request[:(len(request) - 1)] + ')'
        request += ';'
        # print(request)
        self.cursor.execute(request)
        self.conn.commit()

    def set(self, table, data, arguments):       # Таблица(str), данные для изменения(dict): {'имя слобца': 'данные'},
        arguments_t = type(arguments).__name__              # Аргументы для поиска записей(str/list)
        request = 'UPDATE ' + str(table) + '\n'
        request += 'SET '
        for column in data:
            request += str(column) + ' = '
            data_t      = type(data[str(column)]).__name__
            if data_t == 'str':
                request += "'%s'" % (data[str(column)])
            else:
                request += str(data[str(column)])
            request += ','
        request = request[:(len(request) - 1)] + '\n'
        if arguments != '':
            request += '\nWHERE '
            if arguments_t == 'list':
                for argument in arguments:
                    request += argument + ' AND '
                request = request[:(len(request) - 4)]
            if arguments_t == 'str':
                request += arguments
        request += ';'
        self.cursor.execute(request)
        self.conn.commit()

    def delete(self, table, arguments):     # Таблица(str), Аргументы для поиска записей(str/list)
        arguments_t = type(arguments).__name__
        request = 'DELETE\n'
        request += 'FROM ' + str(table) + '\n'
        if arguments != '':
            request += '\nWHERE '
            if arguments_t == 'list':
                for argument in arguments:
                    request += argument + ' AND '
                request = request[:(len(request) - 4)]
            if arguments_t == 'str':
                request += arguments
        request += ';'
        self.cursor.execute(request)
        self.conn.commit()