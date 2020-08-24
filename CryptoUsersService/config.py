import os
from keyring import get_password
from werkzeug.utils import import_string

DB = "users_service"
PORT = 27017
MONGO_IP = "127.0.0.1"
KAFKA_BROKERS = "localhost:9092"
TRANSACTIONS_TOPIC_NAME = "transactions"
USER_SETTINGS_TOPIC_NAME = "user_settings"
USER_NOTIFICATIONS_TOPIC_NAME = "user_notifications"

class BaseConfig(object):
    DEBUG = False
    TESTING = False
    SERVERNAME = "localhost"
    PORT = PORT
    DATABASE = DB
    USERNAME = ""
    PASSWORD = ""
    LOGS_PATH = '../CryptoModel/logs/CryptoModel.log'
    KAFKA_BROKERS = KAFKA_BROKERS
    TRANSACTIONS_TOPIC_NAME = TRANSACTIONS_TOPIC_NAME
    USER_NOTIFICATIONS_TOPIC_NAME = USER_NOTIFICATIONS_TOPIC_NAME
    USER_SETTINGS_TOPIC_NAME = USER_SETTINGS_TOPIC_NAME


class DevelopmentConfig(BaseConfig):
    DEBUG = True
    TESTING = True
    SERVERNAME = "localhost"
    PORT = PORT
    DATABASE = DB
    USERNAME = "test"
    PASSWORD = "test"
    LOGS_PATH = '../CryptoModel/logs/CryptoModel.log'
    KAFKA_BROKERS = KAFKA_BROKERS
    TRANSACTIONS_TOPIC_NAME = TRANSACTIONS_TOPIC_NAME
    USER_NOTIFICATIONS_TOPIC_NAME = USER_NOTIFICATIONS_TOPIC_NAME
    USER_SETTINGS_TOPIC_NAME = USER_SETTINGS_TOPIC_NAME


class ProductionConfig(BaseConfig):
    DEBUG = False
    TESTING = False
    SERVERNAME = MONGO_IP
    PORT = PORT
    DATABASE = DB
    USERNAME = ""
    PASSWORD = ""
    LOGS_PATH = '../CryptoUsersService/logs/CryptoUsersService.log'
    KAFKA_BROKERS = KAFKA_BROKERS
    TRANSACTIONS_TOPIC_NAME = TRANSACTIONS_TOPIC_NAME
    USER_NOTIFICATIONS_TOPIC_NAME = USER_NOTIFICATIONS_TOPIC_NAME
    USER_SETTINGS_TOPIC_NAME = USER_SETTINGS_TOPIC_NAME


config = {
    "development": "CryptoUsersService.config.DevelopmentConfig",
    "production": "CryptoUsersService.config.ProductionConfig",
    "default": "CryptoUsersService.config.DevelopmentConfig",
}


def configure_app():
    config_name = os.getenv('FLASK_ENV', 'CryptoUsersService.config.DevelopmentConfig')
    cfg = import_string(config_name)()
    cfg.USERNAME = get_password('CryptoUsersService', 'USERNAME')
    cfg.PASSWORD = get_password('CryptoUsersService', cfg.USERNAME)
    print(cfg.DATABASE)
    return cfg
