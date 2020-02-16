import sqlite3

class DataBase:
    def __init__(self, data_base_file):
        self.conn = sqlite3.connect(data_base_file, check_same_thread=False)
        self.cursor = self.conn.cursor()

    def request(self, request, args=None):
        if args:
            request_data = self.cursor.execute(request% args).fetchall()
        else:
            request_data = self.cursor.execute(request).fetchall()
        self.conn.commit()
        return request_data