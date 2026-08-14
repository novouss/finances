def test_update_missing_returns_404(client):
    assert (
        client.patch("/transactions/999", json={"description": "nope"}).status_code
        == 404
    )
