def test_update_missing_returns_404(client):
    assert (
        client.patch("/transactions/id/999", json={"description": "nope"}).status_code
        == 404
    )


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
        f"/transactions/id/{created['id']}", json={"description": "edited"}
    )
    assert updated.status_code == 200
    assert updated.json()["description"] == "edited"
    assert updated.json()["amount"] == 10.0
