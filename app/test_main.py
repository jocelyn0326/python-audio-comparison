from random import randbytes
from fastapi.testclient import TestClient
from .main import app
from .constants import BLOCK_SIZE
from .datastore import ds
from random import randbytes, choice
import string
from datetime import datetime
import pytest

timestamp_test = int(datetime.now().timestamp())

DELIVER_API_URI = "/api/data/deliver/"

@pytest.fixture
def channel():
    return ''.join(choice(string.ascii_uppercase + string.digits) for _ in range(30))


@pytest.fixture
def timestamp():
    return int(datetime.now().timestamp())


def test_add_data_to_channel(channel, timestamp):
    with TestClient(app) as client:
        response = client.post(
            DELIVER_API_URI,
            files=dict(
                channel=(None, channel),
                timestamp=(None,  timestamp),
                file=("temp_file", randbytes(BLOCK_SIZE))
            )
        )
        assert response.status_code == 201
        

def test_add_data_to_channel_with_same_timestamp(channel, timestamp):

    with TestClient(app) as client:
        expected_status_codes = (201, 400)
        for expected_status_code in expected_status_codes:
            response = client.post(
                DELIVER_API_URI,
                files=dict(
                    channel=(None, channel),
                    timestamp=(None, timestamp),
                    file=("temp_file", randbytes(BLOCK_SIZE))
                )
            )
            assert response.status_code == expected_status_code



def test_add_data_to_channel_with_wrong_key(channel, timestamp):
    with TestClient(app) as client:
        response = client.post(
            DELIVER_API_URI,
            files=dict(
                wrongkey=(None, channel),
                timestamp=(None, timestamp),
                file=("temp_file", randbytes(BLOCK_SIZE))
            )
        )
        assert response.status_code == 400
        assert response.json() == {"detail": "Invalid request schema"}

def test_add_data_to_channel_with_wrong_size(channel, timestamp):
    with TestClient(app) as client:
        response = client.post(
            DELIVER_API_URI,
            files=dict(
                channel=(None, channel),
                timestamp=(None, timestamp),
                file=("temp_file", randbytes(BLOCK_SIZE*2))
            )
        )
        assert response.status_code == 400
        assert response.json() == {"detail": "Invalid data size"}