def test_home(client):
    r=client.get('/')
    r.status == '200'
