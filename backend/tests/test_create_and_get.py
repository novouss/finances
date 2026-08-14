def test_create_and_get(client):
    created = client.post(
        "/transactions",
        json={
            "date": "2026-08-14",
            "from_account": "Allowance",
            "to_account": "Savings",
            "amount": 150.0,
            "description": "Transfer",
        },
    )
    assert created.status_code == 201
    body = created.json()
    assert body["amount"] == 150.0
    assert body["description"] == "Transfer"
    fetched = client.get(f"/transactions/{body['id']}")
    assert fetched.status_code == 200
    assert fetched.json() == body
