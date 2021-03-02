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


def test_000_get_infos_en(client):
    res = client.get('/info/?lang=en')
    assert res.status_code == 200
    assert res.data == b'This is an example'


def test_001_get_infos_it(client):
    res = client.get('/info/?lang=it')
    assert res.status_code == 200
    assert res.data == b'This is an example'


def test_002_get_infos_wronglang(client):
    res = client.get('/info/?lang=es')
    assert res.status_code == 400


def test_003_get_infos_lang_format(client):
    res = client.get('/info/?lang=it&format=json')
    assert res.status_code == 200
    assert res.data == b'This is an example'


def test_004_get_infos_lang_wrongformat(client):
    res = client.get('/info/?lang=it&format=xml')
    assert res.status_code == 400


def test_010_get_doesnotexist_failed(client):
    res = client.get('/doesnotexist/')
    assert res.status_code == 404


def test_010_get_doesnotexist_failed_noendingslash(client):
    res = client.get('/doesnotexist')
    assert res.status_code == 404


def test_100_v1_get_users(client):
    res = client.get('/v1/users/',headers=HEADERS_V1)
    assert res.status_code == 200


def test_100_v1_get_users_noendingslash(client):
    res = client.get('/v1/users',headers=HEADERS_V1)
    assert res.status_code == 200


def test_100_v1_get_users_doubleendingslashes(client):
    res = client.get('/v1/users//',headers=HEADERS_V1)
    assert res.status_code == 200


def test_101_v1_get_users_failed(client):
    res = client.get('/v1/users')
    assert res.status_code == 406


def test_102_v1_post_auth(client):
    res = client.post('/v1/auth',headers=HEADERS_V1,json={"username" : "mknopfler", "password" : "sultan0FSw1ng"})
    assert res.status_code == 200
    json_data = json.loads(res.data)
    assert "token" in json_data
    assert json_data["token"] == "2b01d9d592da55cca64dd7804bc295e6e03b5df4"


def test_103_v1_post_auth_failed(client):
    res = client.post('/v1/auth',headers=HEADERS_V1)
    assert res.status_code == 400


def test_104_v1_post_user(client):
    headers = HEADERS_V1.copy()
    headers["Authorization"] = "Bearer 2b01d9d592da55cca64dd7804bc295e6e03b5df4"
    res = client.post('/v1/users/',headers=headers,json={"username" : "Paul","email" : "paul@beatles.com"})
    assert res.status_code == 200


def test_105_v1_post_user_failed(client):
    headers = HEADERS_V1.copy()
    headers["Authorization"] = "Bearer 2b01d9d592da55cca64dd7804bc295e6e03b5df4"
    res = client.post('/v1/users',headers=headers)
    assert res.status_code == 400


def test_106_v1_post_user_failed(client):
    res = client.post('/v1/users',headers=HEADERS_V1,json={"username" : "Paul","email" : "paul@beatles.com"})
    assert res.status_code == 406