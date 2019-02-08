import json
def test_index(client):
    response = client.get('/api/v1/')
    assert response.status_code == 200

def test_create_political_party(client):
    payload = {
        "name": "Kanu",
        "hqAddress": "Nakuru",
        "logoUrl": ""
    }
    response = client.post('/api/v1/parties',data = json.dumps(payload), content_type='application/json')
    response_data = response.get_json()
    assert response_data["status"] == 201
    assert response_data["data"]["name"] == "Kanu"
    assert response_data["data"]["hq"] == "Nakuru"
    assert response_data["data"]["logoUrl"] == ""
    assert "id" in response_data["data"]
    

def test_get_political_parties(client):
    response = client.get('/api/v1/parties', content_type='application/json')
    response_data = response.get_json()
    assert len(response_data["data"]) == 1
    assert response_data["data"][0]["name"] == "Kanu"
    assert response_data["data"][0]["hq"] == "Nakuru"
    assert response_data["data"][0]["logoUrl"] == ""
    assert "id" in response_data["data"][0]


def test_get_political_party(client):
    response = client.get('/api/v1/parties/1', content_type='application/json')
    response_data = response.get_json()
    assert "id" in response_data["data"]
    assert response_data["data"]["id"] == 1


def test_delete_political_party(client):
    response = client.delete('/api/v1/parties/1', content_type='application/json')
    response_data = response.get_json()
    assert response_data["data"]["message"] == "political party sucessfully deleted"



def test_create_political_office(client):
    payload = {
        "name": "president",
        "office_type": "federal",
    }

    response = client.post('api/v1/offices',data = json.dumps(payload), content_type = 'application/json')
    response_data = response.get_json()
    assert response_data["status"] == 201
    assert response_data["data"]["name"] == "president"
    assert response_data["data"]["office_type"] == "federal"
    assert "id" in response_data["data"]

def test_get_political_offices(client):
    response = client.get('/api/v1/offices', content_type='application/json')
    response_data = response.get_json()
    assert len(response_data["data"]) == 1
    assert response_data["data"][0]["name"] == "president"
    assert response_data["data"][0]["office_type"] == "federal"
    assert "id" in response_data["data"][0]
  



