import jsonpickle
from flask import jsonify
from CryptoUsersService.helpers import log_error
from kafkaHelper.kafkaHelper import produce, produce_with_key
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

    def get_transactions_before_date(self, user_id, date):
        return jsonify(self.trans_repo.get_transactions_before_date(user_id, date).to_json())

    def insert_transaction(self, user_id, volume, symbol, value, price, date, source, source_id, type,
                           order_type
                           ):
        trans = self.trans_repo.add_transaction(user_id=user_id, volume=volume, symbol=symbol, value=value,
                                                price=price, source=source, currency=CURRENCY, source_id=source_id,
                                                transaction_type = type, order_type= order_type, date=date)

        self.trans_repo.commit()

        return trans

    def update_transaction(self, id, user_id, volume, symbol, value, price, date, source, source_id,  type,
                           order_type ):
        trans = self.trans_repo.add_transaction(id, user_id, volume, symbol, value, price, CURRENCY, date, source,
                                                source_id=source_id,transaction_type=type, order_type=order_type )

        self.trans_repo.commit()
        return trans

    def get_user_notifications(self, items_count):
        return jsonify(self.trans_repo.fetch_notifications(items_count).to_json())

    def get_user_channels(self, user_id, channel_type):
        return jsonify(self.trans_repo.fetch_user_channels(user_id, channel_type).to_json())

    def get_user_settings(self, user_id):
        return jsonify(self.users_repo.get_user_settings(user_id).to_json())

    def insert_user_notification(self, user_id, user_name, user_email, start_date, end_date,
                                 check_every, is_active, channel_type, notification_type, threshold_value, source_id):
        un = self.users_repo.add_notification(user_id=user_id, user_name=user_name, user_email=user_email,
                                              start_date=start_date, end_date=end_date,
                                              check_every=check_every,
                                              is_active=is_active, channel_type=channel_type,
                                              notification_type=notification_type,
                                              threshold_value=threshold_value, source_id=source_id)
        self.users_repo.commit()
        return un

    def insert_user_settings(self, user_id, preferred_currency, source_id):
        us = self.users_repo.add_user_settings(user_id=user_id, preferred_currency=preferred_currency,
                                               source_id=source_id)
        self.users_repo.commit()
        return us
