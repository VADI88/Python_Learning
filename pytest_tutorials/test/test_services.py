import pytest
import requests

import source.service as services
import unittest.mock as mock


@mock.patch("source.service.get_user_from_db")
def test_get_user_from_db(mock_get_user_from_db):
    mock_get_user_from_db.return_value = "Mocked Alice"
    user_name = services.get_user_from_db(1)
    assert user_name == "Mocked Alice"




@mock.patch("requests.get")
def test_get_users(mock_get):
    mock_responses = mock.Mock()
    mock_responses.status_code = 200
    mock_responses.json.return_value = {"id": 1 , "name": "John Doe"}
    mock_get.return_value = mock_responses
    data = services.get_user()
    assert data == {"id": 1 , "name": "John Doe"}


@mock.patch("requests.get")
def test_get_users_error(mock_get):
    mock_responses = mock.Mock()
    mock_responses.status_code = 400
    mock_get.return_value = mock_responses
    with pytest.raises(requests.HTTPError):
        services.get_user()



