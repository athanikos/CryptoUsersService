import os
from keyring import get_password
from werkzeug.utils import import_string

DB = "crypto"
PORT = 27017
MONGO_IP = "134.122.79.43"


class BaseConfig(object):
    DEBUG = False
    TESTING = False
    SERVERNAME = "localhost"
    PORT = PORT
    DATABASE = DB
    USERNAME = ""
    PASSWORD = ""
    LOGS_PATH = '../CryptoModel/logs/CryptoModel.log'


class DevelopmentConfig(BaseConfig):
    DEBUG = True
    TESTING = True
    SERVERNAME  = "localhost"
    PORT = PORT
    DATABASE = "test_crypto"
    USERNAME = "test"
    PASSWORD = "test"
    LOGS_PATH ='../CryptoModel/logs/CryptoModel.log'


class ProductionConfig(BaseConfig):
    DEBUG = False
    TESTING = False
    SERVERNAME = MONGO_IP
    PORT = PORT
    DATABASE = DB
    USERNAME = ""
    PASSWORD = ""
    LOGS_PATH = '../CryptoUsersService/logs/CryptoUsersService.log'


config = {
    "development": "CryptoUsersService.config.DevelopmentConfig",
    "production": "CryptoUsersService.config.ProductionConfig",
    "default": "CryptoUsersService.config.DevelopmentConfig",
}


def configure_app():
    config_name = os.getenv('FLASK_ENV', 'default')
    cfg = import_string(config_name)()
    cfg.USERNAME = get_password('CryptoUsersService',  'USERNAME')
    print(cfg.USERNAME)
    cfg.PASSWORD = get_password('CryptoUsersService',    cfg.USERNAME)
    print(cfg.PASSWORD)
    return cfg