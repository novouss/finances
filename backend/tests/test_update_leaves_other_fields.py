def test_update_leaves_other_fields(client):
    created = client.post(
        "/transactions",
        json={
            "date": "2026-08-14",
            "from_account": "Allowance",
            "to_account": "Transport",
            "amount": 10.0,
        },
    ).json()
    updated = client.patch(
        f"/transactions/{created['id']}", json={"description": "edited"}
    )
    assert updated.status_code == 200
    assert updated.json()["description"] == "edited"
    assert updated.json()["amount"] == 10.0
