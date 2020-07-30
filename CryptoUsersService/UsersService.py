import jsonpickle
from flask import jsonify
from CryptoUsersService.helpers import log_error
from kafkaHelper.kafkaHelper import produce
from cryptodataaccess.Transactions.TransactionRepository import TransactionRepository
from cryptodataaccess.Transactions.TransactionMongoStore import TransactionMongoStore
from cryptodataaccess.Users.UsersRepository import UsersRepository
from cryptodataaccess.Users.UsersMongoStore import UsersMongoStore

DATE_FORMAT = "%Y-%m-%d"
CURRENCY = "EUR"


class UsersService:

    def __init__(self, config):
        self.users_store = UsersMongoStore(config, log_error)
        self.transactions_store = TransactionMongoStore(config, log_error)
        self.trans_repo = TransactionRepository(self.transactions_store)
        self.users_repo = UsersRepository(self.users_store)

    def get_transactions(self, user_id):
        return jsonify(self.trans_repo.get_transactions(user_id).to_json())

    def insert_transaction(self, user_id, volume, symbol, value, price, date, source, source_id, operation):
        trans = self.trans_repo.add_transaction(user_id=user_id, volume=volume, symbol=symbol, value=value,
                                                price=price,
                                                date=date, source=source, currency=CURRENCY, source_id=source_id)

        self.trans_repo.commit()

        produce(broker_names=self.transactions_store.configuration.KAFKA_BROKERS,
                topic=self.transactions_store.configuration.TRANSACTIONS_TOPIC_NAME
                , data_item=jsonpickle.encode(trans))
        return trans

    def update_transaction(self, id, user_id, volume, symbol, value, price, date, source, source_id, operation):
        trans = self.trans_repo.add_transaction(id, user_id, volume, symbol, value, price, CURRENCY, date, source,
                                                source_id=source_id)

        self.trans_repo.commit()
        return trans

    def get_user_notifications(self, items_count):
        return jsonify(self.trans_repo.fetch_notifications(items_count).to_json())

    def get_user_channels(self, user_id, channel_type):
        return jsonify(self.trans_repo.fetch_user_channels(user_id, channel_type).to_json())

    def insert_user_notification(self, user_id, user_name, user_email, expression_to_evaluate, check_every_seconds,
                                 check_times, is_active, channel_type, fields_to_send, source_id):
        un = self.users_repo.add_notification(user_id, user_name, user_email, expression_to_evaluate,
                                              check_every_seconds,
                                              check_times, is_active, channel_type, fields_to_send, source_id)
        produce(broker_names=self.users_store.configuration.KAFKA_BROKERS,
                topic=self.users_store.configuration.USER_NOTIFICATIONS_TOPIC_NAME
                , data_item=jsonpickle.encode(un))
        return un

    def insert_user_channel(self, user_id, channel_type, chat_id, source_id):
        return self.users_repo.add_user_channel(user_id, channel_type, chat_id, source_id)
