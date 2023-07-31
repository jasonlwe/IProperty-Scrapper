# Credits: Ceciput

from configparser import ConfigParser
import mysql.connector

config = ConfigParser()
config.sections()
config.read('config.ini')

DB_HOST = config['MYSQL']["HOST"]
DB_USERNAME = config['MYSQL']["USERNAME"]
DB_PASSWORD = config['MYSQL']["PASSWORD"]
DB_DATABASE = config['MYSQL']["DATABASE"]
DB_PORT = config['MYSQL']["PORT"]

# SQL_ATTR_CONNECTION_TIMEOUT = 113
login_timeout = 1


# connection_timeout = 3

class MYSQL():

    def __init__(self,
                 hostname=DB_HOST,
                 username=DB_USERNAME,
                 password=DB_PASSWORD,
                 database=DB_DATABASE,
                 port=DB_PORT
                 ):
        self.hostname = hostname
        self.username = username
        self.password = password
        self.database = database
        self.port = port

        self.conn = mysql.connector.connect(host=self.hostname,
                                            user=self.username,
                                            password=self.password,
                                            database=self.database,
                                            port=self.port)
        self.cur = self.conn.cursor()

    def query(self, sql, args=(), one=False):
        self.cur.execute(sql, args)
        r = [dict((self.cur.description[i][0], value) \
                  for i, value in enumerate(row)) for row in self.cur.fetchall()]
        return (r[0] if r else None) if one else r

    def execute(self, sql, args=()):
        self.cur.execute(sql, args)

    def commit(self):
        self.conn.commit()

    def close(self):
        self.cur.close()
        self.conn.close()
