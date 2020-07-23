import jsonpickle
from flask import jsonify
from CryptoUsersService.helpers import log_error
from kafkaHelper.kafkaHelper import produce
DATE_FORMAT = "%Y-%m-%d"
CURRENCY = "EUR"
from cryptodataaccess.TransactionRepository import  TransactionRepository
from cryptodataaccess.Repository import  Repository


class UsersService:

    def __init__(self, config):
        self.repo = Repository(config, log_error)
        self.trans_repo = TransactionRepository(config, log_error)

    def get_transactions(self, user_id):
        return jsonify(self.trans_repo.fetch_transactions(user_id).to_json())

    def insert_transaction(self, user_id, volume, symbol, value, price, date, source, source_id, operation):
        trans =self.trans_repo.insert_transaction(user_id=user_id, volume=volume, symbol=symbol, value=value, price=price,
                                        date=date, source=source, currency=CURRENCY, source_id= source_id, operation=operation)
        produce(broker_names=self.repo.configuration.KAFKA_BROKERS, topic=self.repo.configuration.TRANSACTIONS_TOPIC_NAME
                            , data_item=jsonpickle.encode(trans))
        return trans

    def update_transaction(self, id, user_id, volume, symbol, value, price, date, source, source_id, operation):
        return self.trans_repo.update_transaction(id, user_id, volume, symbol, value, price, CURRENCY, date, source, source_id= source_id, operation=operation)

    def get_user_notifications(self, items_count):
        return jsonify(  self.repo.fetch_notifications(items_count).to_json())

    def get_user_channels(self, user_id, channel_type):
         return jsonify(  self.repo .fetch_user_channels(user_id, channel_type).to_json())

    def insert_user_notification(self, user_id, user_name, user_email, condition_value, field_name, operator,
                                 notify_times,
                                 notify_every_in_seconds, symbol, channel_type):
         return   self.repo .insert_notification(user_id, user_name, user_email, condition_value, field_name, operator,
                                        notify_times,
                                        notify_every_in_seconds, symbol, channel_type)

    def insert_user_channel(self, user_id, channel_type, chat_id):
         return   self.repo .insert_user_channel(user_id, channel_type, chat_id)
