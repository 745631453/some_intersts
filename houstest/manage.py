from flask_script import Manager
from utlis.App import creat_app
from utlis.config import Config

app = creat_app(Config)

manage = Manager(app=app)

if __name__ == '__main__':
    manage.run()
