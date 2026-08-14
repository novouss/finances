def test_delete_and_404(client):
    created = client.post(
        "/transactions",
        json={
            "date": "2026-08-14",
            "from_account": "Bills",
            "to_account": "August 2026",
            "amount": 5.0,
        },
    ).json()
    assert client.delete(f"/transactions/{created['id']}").status_code == 204
    assert client.get(f"/transactions/{created['id']}").status_code == 404
    assert client.delete("/transactions/999").status_code == 404
