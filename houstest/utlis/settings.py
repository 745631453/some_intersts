from utlis.funcktions import creat_data
import os

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
stat_dir = os.path.join(BASE_DIR, 'static')
templates_dir = os.path.join(BASE_DIR, 'templates')

DATABASE = {
    'user': 'root',
    'password': '147258',
    'db': 'mysql',
    'driver': 'pymysql',
    'port': '3306',
    'host': '127.0.0.1',
    'name': 's_aj',
}

SQLALCHEMY_DATABASE_URI = creat_data(DATABASE)

UPLOAD_DIR = os.path.join(os.path.join(BASE_DIR, 'static'), 'upload')
