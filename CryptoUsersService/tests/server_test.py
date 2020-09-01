import pytest
import json

from bson import ObjectId

from server import configure_app, create_app
from cryptodataaccess.helpers import do_connect
from cryptomodel.cryptostore import user_transaction, user_settings, user_notification


@pytest.fixture(scope='module')
def test_client():
    flask_app = create_app()
    testing_client = flask_app.test_client()
    ctx = flask_app.app_context()
    ctx.push()
    yield testing_client  # this is where the testing happens!
    ctx.pop()


def test_fetch_transactions(test_client):
    config = configure_app()
    do_connect(config)
    user_transaction.objects.all().delete()
    ut = user_transaction()
    ut.symbol = "BTC"
    ut.date = "2020-01-01"
    ut.price = 10
    ut.value = 1
    ut.user_id = 1
    ut.volume = 10
    ut.currency = "EUR"
    ut.source = "kraken"
    ut.operation = "Added"
    ut.source_id = ObjectId('666f6f2d6261722d71757578')
    ut.save(force_insert=True, validate=False, clean=False)
    response = test_client.get('/api/v1/transactions/1')
    data_json2 = json.loads(response.get_json(silent=True, force=True))
    assert response.status_code == 200


def test_fetch_user_settings_by_user_id(test_client):
    config = configure_app()
    do_connect(config)
    user_settings.objects.all().delete()
    us = user_settings()
    us.preferred_currency = "EUR"
    us.source_id = ObjectId('666f6f2d6261722d71757578')
    us.user_id = 1
    us.save(force_insert=True, validate=False, clean=False)
    response = test_client.get('/api/v1/user-settings/1')
    data_json2 = json.dumps(response.get_json(silent=True, force=True))
    assert response.status_code == 200


def test_insert_user_notification(test_client):
    config = configure_app()
    do_connect(config)
    user_notification.objects.all().delete()

    response = test_client.post('/api/v1/user-notification',
                                data=json.dumps(
                                    {
                                        'user_id': 2,
                                        'user_name': '1',
                                        'user_email': 'sdsds',
                                        'start_date': '2020-06-20',
                                        'end_date': '2020-06-20',
                                        'check_every': '00:01',
                                        'is_active': True,
                                        'channel_type': 'TELEGRAM',
                                        'threshold_value': 1,
                                        'operation': 'ADDED',
                                        'source_id': '',
                                        'notification_type': 'BALANCE'
                                    }
                                ),
                                content_type='application/json',
                                )

    data_json2 = json.loads(response.get_json(silent=True, force=True))
    assert response.status_code == 200
    assert (len(user_notification.objects) == 1)
