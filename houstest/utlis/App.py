from flask import Flask

from utlis.settings import stat_dir, templates_dir

from utlis.funcktions import creat_a
from userapp.user_views import user
from userapp.house_views import house
from userapp.order_views import order


def creat_app(config):
    app = Flask(__name__, static_folder=stat_dir, template_folder=templates_dir)
    app.register_blueprint(blueprint=user, url_prefix='/user')
    app.register_blueprint(blueprint=house, url_prefix='/house')
    app.register_blueprint(blueprint=order, url_prefix='/order')

    creat_a(app)
    app.config.from_object(config)


    return app
