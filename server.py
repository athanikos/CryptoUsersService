import pymongo
from flask import Flask, jsonify, request
from flask.blueprints import Blueprint
from CryptoUsersService.config import configure_app
from CryptoUsersService.UsersService import UsersService

bp = Blueprint(__name__.split('.')[0], __name__.split('.')[0])


def create_app():
    the_app = Flask(__name__.split('.')[0], instance_relative_config=True)
    configure_app()
    the_app.register_blueprint(bp)
    return the_app


@bp.route("/api/v1/prices",
          methods=['GET'])
def get_prices():
    ps = UsersService(configure_app())
    return ps.get_prices(items_count=10)


@bp.route("/api/v1/transactions/<int:user_id>",
          methods=['GET'])
def get_transactions(user_id):
    ts = UsersService(configure_app())
    return ts.get_transactions(user_id)


@bp.route("/api/v1/transaction",
          methods=['POST'])
def insert_transaction():
    ts = UsersService(configure_app())

    if request.json['source_id'] == '':
        sc_id = None
    else:
        sc_id = request.json['source_id']

    un = ts.insert_transaction(request.json['user_id'], request.json['volume'], request.json['symbol'],
                               request.json['value'], request.json['price'], request.json['date'],
                               request.json['source'], sc_id, request.json['type'], request.json['order_type'] )
    return jsonify(un.to_json())


@bp.route("/api/v1/transaction",
          methods=['PUT'])
def update_transaction():
    ts = UsersService(configure_app())
    un = ts.update_transaction(request.json['id'],
                               request.json['user_id'], request.json['volume'], request.json['symbol'],
                               request.json['value'], request.json['price'], request.json['date'],
                               request.json['source'], request.json['source_id'], request.json['type'], request.json['order_type'] )
    return jsonify(un.to_json())


@bp.route("/api/v1/balance/<int:user_id>",
          methods=['GET'])
def get_balance(user_id):
    bs = UsersService(configure_app())
    return bs.compute(user_id)


@bp.route("/api/v1/user-channels/<int:user_id>/<string:channel_type>",
          methods=['GET'])
def get_user_channels(user_id, channel_type):
    uns = UsersService(configure_app())
    return uns.get_user_channels(user_id, channel_type)


@bp.route("/api/v1/user-notifications",
          methods=['GET'])
def get_user_notifications():
    uns = UsersService(configure_app())
    return uns.get_user_notifications(10)


@bp.route("/api/v1/user-settings/<int:user_id>",
          methods=['GET'])
def get_user_settings(user_id):
    uns = UsersService(configure_app())
    return uns.get_user_settings(user_id)


@bp.route("/api/v1/user-notification",
          methods=['POST'])
def insert_notification():
    uns = UsersService(configure_app())

    if request.json['source_id'] == '':
        sc_id = None
    else:
        sc_id = request.json['source_id']

    un = uns.insert_user_notification(
        user_id=request.json['user_id'],
        user_name=request.json['user_name'],
        user_email=request.json['user_email'],
        check_every=request.json['check_every'],
        start_date=request.json['start_date'],
        end_date=request.json['end_date'],
        notification_type =request.json['notification_type'],
        channel_type=request.json['channel_type'],
        source_id=sc_id,
        is_active=request.json['is_active'],
        threshold_value=request.json['threshold_value']
    )
    return jsonify(un.to_json())


@bp.route("/api/v1/user-channel",
          methods=['POST'])
def insert_user_channel():
    uns = UsersService(configure_app())
    if request.json['source_id'] == '':
        sc_id = None
    else:
        sc_id = request.json['source_id']

    un = uns.insert_user_channel(request.json['user_id'], request.json['channel_type'], request.json['chat_id'], sc_id)

    return jsonify(un.to_json())


@bp.route("/api/v1/user-settings",
          methods=['POST'])
def insert_user_settings():
    if request.json['source_id'] == '':
        sc_id = None
    else:
        sc_id = request.json['source_id']

    uns = UsersService(configure_app())
    un = uns.insert_user_settings(
        user_id=request.json['userId'], source_id=sc_id, preferred_currency=request.json['preferred_currency'])

    return jsonify(un.to_json())


@bp.app_errorhandler(pymongo.errors.ServerSelectionTimeoutError)
def handle_error(error):
    message = [str(x) for x in error.args]
    status_code = 500
    success = False
    response = {
        'success': success,
        'error': {
            'type': error.__class__.__name__,
            'message': message
        }
    }

    return jsonify(response), status_code


if __name__ == '__main__':
    create_app().run(port=5100)
