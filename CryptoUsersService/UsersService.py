import jsonpickle
from flask import jsonify
from CryptoUsersService.data_access.Repository import Repository
from CryptoUsersService.helpers import log_error
from kafkaHelper.kafkaHelper import produce_with_action

DATE_FORMAT = "%Y-%m-%d"
CURRENCY = "EUR"


class UsersService:

    def __init__(self, config):
        self.repo = Repository(config, log_error)

    def get_transactions(self, user_id):
        repo = Repository(self.repo.configuration, log_error)
        return jsonify(repo.fetch_transactions(user_id).to_json())

    def insert_transaction(self, user_id, volume, symbol, value, price, date, source):
        repo = Repository(self.repo.configuration, log_error)
        trans = repo.insert_transaction(user_id=user_id, volume=volume, symbol=symbol, value=value, price=price,
                                        date=date, source=source, currency=CURRENCY)

        produce_with_action(broker_names=self.repo.configuration.KAFKA_BROKERS, topic=self.repo.configuration.TRANSACTIONS_TOPIC_NAME
                            , data_item=jsonpickle.encode(trans))
        return trans

    def update_transaction(self, id, user_id, volume, symbol, value, price, date, source):
        repo = Repository(self.repo.configuration, log_error)
        return repo.update_transaction(id, user_id, volume, symbol, value, price, CURRENCY, date, source)

    def get_user_notifications(self, items_count):
        repo = Repository(self.repo.configuration)
        return jsonify(repo.fetch_notifications(items_count).to_json())

    def get_user_channels(self, user_id, channel_type):
        repo = Repository(self.repo.configuration)
        return jsonify(repo.fetch_user_channels(user_id, channel_type).to_json())

    def insert_user_notification(self, user_id, user_name, user_email, condition_value, field_name, operator,
                                 notify_times,
                                 notify_every_in_seconds, symbol, channel_type):
        repo = Repository(self.repo.configuration)
        return repo.insert_notification(user_id, user_name, user_email, condition_value, field_name, operator,
                                        notify_times,
                                        notify_every_in_seconds, symbol, channel_type)

    def insert_user_channel(self, user_id, channel_type, chat_id):
        repo = Repository(self.repo.configuration)
        return repo.insert_user_channel(user_id, channel_type, chat_id)
