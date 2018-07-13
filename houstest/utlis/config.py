from utlis.settings import SQLALCHEMY_DATABASE_URI
import redis


class Config:
    SQLALCHEMY_DATABASE_URI = SQLALCHEMY_DATABASE_URI
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    # 配置session
    SECRET_KEY = 'secret_key'
    SESSION_TYPE = 'redis'
    SESSION_REDIS = redis.Redis(host='127.0.0.1', port='6379')
    SESSION_KEY_PREFIX = 'test'
