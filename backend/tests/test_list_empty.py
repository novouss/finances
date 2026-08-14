def test_list_empty(client):
    response = client.get("/transactions")
    assert response.status_code == 200
    assert response.json() == []
