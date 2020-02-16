import sqlite3

class DataBase:
    def __init__(self, data_base_file):
        self.conn = sqlite3.connect(data_base_file, check_same_thread=False)
        self.cursor = self.conn.cursor()

    def request(self, request, args=None):
        if args:
            args_to_add = ()
            if type(args).__name__ == 'tuple' or type(args).__name__ == 'list':
                for arg in args:
                    args_to_add += (arg.replace('"', '&#34;').replace("'", '&#39;'), )
            elif type(args).__name__ == 'str':
                args_to_add = (args.replace('"', '&#34;').replace("'", '&#39;'))
            request_data = self.cursor.execute(request% args_to_add).fetchall()
        else:
            request_data = self.cursor.execute(request).fetchall()
        self.conn.commit()
        return request_data