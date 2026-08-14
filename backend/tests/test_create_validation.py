def test_create_validation(client):
    assert client.post("/transactions", json={"amount": 1.0}).status_code == 422
    assert (
        client.post(
            "/transactions", json={"date": "2026-08-14", "amount": -5.0}
        ).status_code
        == 422
    )
