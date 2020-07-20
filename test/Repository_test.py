import mock
from bson import ObjectId
from pymongo.errors import ServerSelectionTimeoutError
from CryptoUsersService.config import configure_app
from dataaccess.Repository import Repository
import pytest
from dataaccess import helpers
from cryptomodel.cryptomodel import *


@pytest.fixture(scope='module')
def mock_log():
    with mock.patch("CryptoUsersService.helpers.log_error"
                    ) as _mock:
        _mock.return_value = True
        yield _mock


def test_insert_user_channel():
    config = configure_app()
    repo = Repository(config, mock_log)
    helpers.do_connect(config)
    user_channel.objects.all().delete()
    uc = repo.insert_user_channel(1, 'da', '1')
    assert (uc.channel_type == 'da')


def test_log_when_do_connect_raises_exception(mock_log):
    with mock.patch("dataaccess.helpers.do_connect"
                    ) as _mock:
        _mock.side_effect = ServerSelectionTimeoutError("hi")
        with mock.patch("dataaccess.helpers.log_error") as log:
            with pytest.raises(ServerSelectionTimeoutError):
                repo = Repository(configure_app(), mock_log)
                repo.insert_user_channel(1, "telegram", chat_id="1")
            mock_log.assert_called()


def test_insert_transaction():
    config = configure_app()
    repo = Repository(config, mock_log)
    helpers.do_connect(config)
    user_transaction.objects.all().delete()
    ut = repo.insert_transaction(1, 1, 'OXT', 1, 1, "USD", "2020-01-01", "kraken")
    assert (ut.user_id == 1)
    assert (ut.symbol == "OXT")
    assert (len(user_transaction.objects) == 1)


def test_update_transaction():
    config = configure_app()
    repo = Repository(config, mock_log)
    helpers.do_connect(config)
    user_transaction.objects.all().delete()
    ut = repo.insert_transaction(1, 1, 'OXT', 1, 1, "USD", "2020-01-01", "kraken")
    ut = repo.update_transaction(ut.id, 1, 1, 'OXT2', 1, 1, "EUR", "2020-01-01", "kraken")
    assert (ut.user_id == 1)
    assert (ut.symbol == "OXT2")
    assert (ut.currency == "EUR")


def test_update_transaction_when_does_not_exist_throws_ValueError():
    config = configure_app()
    repo = Repository(config, mock_log)
    helpers.do_connect(config)
    user_transaction.objects.all().delete()
    with pytest.raises(ValueError):
        repo.update_transaction(ObjectId('666f6f2d6261722d71757578'), 1, 1, 'OXT', "EUR", 1, 1, "2020-01-01",
                                     "kraken")


def test_update_notification_when_does_not_exist_throws_ValueError():
    config = configure_app()
    repo = Repository(config, mock_log)
    helpers.do_connect(config)
    user_notification.objects.all().delete()
    with pytest.raises(ValueError):
        repo.update_notification(ObjectId('666f6f2d6261722d71757578'), 1, 'nik', "nik@test.com", 1, "field_name",
                                      ">",1,1,"OXT","telegram")


def test_update_notification():
    config = configure_app()
    repo = Repository(config, mock_log)
    helpers.do_connect(config)
    user_notification.objects.all().delete()

    un = repo.insert_notification( 1, 'nik', "nik@test.com", 1, "field_name",
                                      ">",1,1,"OXT","telegram")
    un = repo.update_notification(un.id,  1, 'nik2', "nik@test.com", 1, "field_name",
                                      ">",1,1,"OXT","telegram")
    assert (un.user_name == "nik2")


def test_delete_transaction_when_does_not_exist_throws_ValueError():
    config = configure_app()
    repo = Repository(config, mock_log)
    helpers.do_connect(config)
    user_transaction.objects.all().delete()
    with pytest.raises(ValueError):
        repo.delete_transaction(ObjectId('666f6f2d6261722d71757578'))


def test_delete_transaction_when_exists():
    config = configure_app()
    repo = Repository(config, mock_log)
    helpers.do_connect(config)
    ut = repo.insert_transaction(1, 1, 'OXT', 1, 1, "EUR", "2020-01-01", "kraken")
    assert (len(user_transaction.objects) == 1)
    ut = repo.delete_transaction(ut.id)
    assert (len(user_transaction.objects) == 0)


def test_delete_notification_when_exists():
    config = configure_app()
    repo = Repository(config, mock_log)
    helpers.do_connect(config)
    user_notification.objects.all().delete()
    ut = repo.insert_notification(1, 'nik', 'nik@OXT.com', 100, 'field1', ">", 1, 1,"OXT","telegram")
    assert (len(user_notification.objects) == 1)
    ut = repo.delete_notification(ut.id)
    assert (len(user_notification.objects) == 0)



