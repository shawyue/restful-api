# _*- coding:utf-8 _*_

import pymysql.cursors
import time
from logbook import Logger

log = Logger("test")
class MySQLClient(object):

    def __init__(self, config):
        self.host = config.get("MYSQL_HOST", "192.168.190.147")
        self.port = config.get("MYSQL_PORT", 3306)
        self.user = config.get("MYSQL_USER", "restful")
        self.password = config.get("MYSQL_PASSWORD", "restful")
        self.db = config.get("MYSQL_DB", "restful")
        self.charset = config.get("MYSQL_CHARSET", "utf8")
        
        self.connect()

    def connect(self):
        try:
            self.connection = pymysql.connect(
                                            host=self.host,
                                            port=self.port,
                                            user=self.user,
                                            password=self.password,
                                            db=self.db,
                                            charset=self.charset
                                            )
            self.write_cursor = self.connection.cursor()
            self.read_cursor = self.connection.cursor()
            return  self.connection
        except Exception as e:
            log.error('\n' + str(e) + '\n')
        

    def execute(self, sql, args, cursor = None):

        if(cursor):
            rows = cursor.execute(query=sql, args=args)
        else:
            rows = self.write_cursor.execute(query=sql, args=args)
        return rows

    def execute_many(self, sql, args):
        rows = self.write_cursor.executemany(sql, args)
        return rows

    def fetch_all(self, sql, args = None):
        self.execute(sql=sql, args=args, cursor=self.read_cursor)
        return self.read_cursor.fetchall()

    def fetch_many(self, sql=None, args=None, size=1):
        if(sql):
            self.execute(sql=sql, args=args, cursor=self.read_cursor)
            return self.read_cursor.fetchmany(size)
        else:
            return self.read_cursor.fetchmany(size)

    def fetch_one(self, sql=None, args=None):
        if(sql):
            self.execute(sql=sql, args=args, cursor=self.read_cursor)
            return self.read_cursor.fetchone()
        else:
            return self.read_cursor.fetchone()

    def commit(self):
        return self.connection.commit()

    def rollback(self):
        return self.connection.rollback()

    def begin_transaction(self):
        return self.connection.begin()

    def select_db(self, db):
        self.connection.select_db(db)

    def close_connect(self):
        self.connection.commit()
        self.write_cursor.close()
        self.read_cursor.close()
        self.connection.close()
        return None

    def ping_server(self):
        try:
            self.connection.ping()
        except Exception as e:
            log.error('\n' + str(e) + '\n')
            time.sleep(2)
            self.ping_server()


mysql_client = MySQLClient({})
class GenerateArticleID(object):

    def __new__(cls):
        
        if not hasattr(cls, 'instance'):
            cls.instance = super(GenerateArticleID, cls).__new__(cls)
        return cls.instance

    def __init__(self):
        self.get_max_id()


    def get(self):
        if self.max_article_id == None:
            self.max_article_id = 1000
            return self.max_article_id
        else:
            self.max_article_id = self.max_article_id + 1
            return self.max_article_id

    def get_max_id(self):
        self.max_article_id = mysql_client.fetch_one("SELECT MAX(ID) FROM ARTICLES")[0]
        return self.max_article_id

if __name__ == "__main__":
    id_obj = GenerateArticleID()
    print(id_obj.get())
    print(id_obj.get())
    id_obj1 = GenerateArticleID()
    print("id_obj1",id_obj1.get())
    print("id_obj",id_obj.get())
    print("id_obj1",id_obj1.get())


    