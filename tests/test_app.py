from flask import json
from random import randrange
from app import app



def test_home(client):
    r = client.get('/')
    assert r.status_code == 200

def test_users_post(client):
    n = randrange(0,999999)
    n_string = str(n)
    global username
    username = 'zaza'+n_string
    global email
    email = 'zaza@zaza.com'+n_string
    j = {'username': username, 'email': email}
    r = client.post('/users', data=json.dumps(j), content_type='application/json')
    assert r.status_code == 200
    assert r.json['id'] is not None
    assert type(r.json['id']) is int
    global user_id
    user_id = str(r.json['id'])
    assert r.json['username'] is not None
    assert type(r.json['username']) is str
    assert r.json['username'] == username
    assert r.json['email'] is not None
    assert type(r.json['email']) is str
    assert r.json['email'] == email
    r = client.post('/users', data=json.dumps(j), content_type='application/json')
    assert r.status_code == 400

def test_users_get(client):
    r=client.get('/users')
    assert r.status_code == 200

def test_users_get_id(client):
    r = client.get("/users/"+user_id)
    assert r.status_code == 200
    r = client.get("/users/999")
    assert r.status_code == 404

def test_users_put(client):
    username_modified = username+"modified"
    email_modified = email+"modified"

    j = {'id': int(user_id), 'username': username_modified, 'email': email_modified}
    r = client.put("/users", data=json.dumps(j), content_type='application/json')
    assert r.status_code == 200
    assert r.json['id'] is not None
    assert type(r.json['id']) is int
    assert r.json['username'] is not None
    assert type(r.json['username']) is str
    assert r.json['username'] == username_modified
    assert r.json['email'] is not None
    assert type(r.json['email']) is str
    assert r.json['email'] == email_modified


def test_users_delete(client):
    r = client.delete("/users/"+user_id)
    assert r.status_code == 200
    r = client.delete("/users/999")
    assert r.status_code == 404
