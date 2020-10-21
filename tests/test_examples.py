# -*- coding: utf-8 -*-

__license__ = "Apache-2.0"
__author__ = "Jean-Christophe Fabre <jean-christophe.fabre@inrae.fr>"


import pytest
import rejocker
import json


HEADERS_V1 = {"Accept" : "application/x.rejocker+json;version=1.0"}


@pytest.fixture
def client():
    rejocker.app.config['TESTING'] = True

    with rejocker.app.test_client() as client:
        yield client


def test_00_get_infos(client):
    res = client.get('/info/')
    assert res.status_code == 200
    assert res.data == b'This is an example'


def test_01_get_doesnotexist_failed(client):
    res = client.get('/doesnotexist/')
    assert res.status_code == 404


def test_10_v1_get_users(client):
    res = client.get('/v1/users/',headers=HEADERS_V1)
    assert res.status_code == 200


def test_11_v1_get_users_failed(client):
    res = client.get('/v1/users/')
    assert res.status_code == 406


def test_12_v1_post_auth(client):
    res = client.post('/v1/auth/',headers=HEADERS_V1,json={"username" : "mknopfler", "password" : "sultan0FSw1ng"})
    assert res.status_code == 200
    json_data = json.loads(res.data)
    assert "token" in json_data
    assert json_data["token"] == "2b01d9d592da55cca64dd7804bc295e6e03b5df4"


def test_13_v1_post_auth_failed(client):
    res = client.post('/v1/auth/',headers=HEADERS_V1)
    assert res.status_code == 400


def test_14_v1_post_user(client):
    headers = HEADERS_V1.copy()
    headers["Authorization"] = "Bearer 2b01d9d592da55cca64dd7804bc295e6e03b5df4"
    res = client.post('/v1/users/',headers=headers,json={"username" : "Paul","email" : "paul@beatles.com"})
    assert res.status_code == 200


def test_15_v1_post_user_failed(client):
    headers = HEADERS_V1.copy()
    headers["Authorization"] = "Bearer 2b01d9d592da55cca64dd7804bc295e6e03b5df4"
    res = client.post('/v1/users/',headers=headers)
    assert res.status_code == 400


def test_16_v1_post_user_failed(client):
    res = client.post('/v1/users/',headers=HEADERS_V1,json={"username" : "Paul","email" : "paul@beatles.com"})
    assert res.status_code == 406