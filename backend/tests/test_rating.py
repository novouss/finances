def test_rating_math(client):
    client.post(
        "/transactions",
        json={
            "date": "2026-08-01",
            "from_account": "Salary",
            "to_account": "Allowance",
            "amount": 10000,
        },
    )
    expenses = [100, 50, 25, 25]
    for i, amount in enumerate(expenses):
        client.post(
            "/transactions",
            json={
                "date": f"2026-08-{i + 1:02d}",
                "from_account": "Allowance",
                "to_account": "Food",
                "amount": amount,
            },
        )
    r = client.get("/transactions/rating", params={"from_account": "Allowance"}).json()
    assert r["rating"] == 5
    client.post(
        "/transactions",
        json={
            "date": "2026-08-05",
            "from_account": "Allowance",
            "to_account": "Food",
            "amount": 2000,
        },
    )
    r = client.get("/transactions/rating", params={"from_account": "Allowance"}).json()
    assert r["rating"] == 1


def test_rating_zeroes(client):
    client.post(
        "/transactions",
        json={
            "date": "2026-08-01",
            "from_account": "Salary",
            "to_account": "Allowance",
            "amount": 10000,
        },
    )
    r = client.get("/transactions/rating", params={"from_account": "Allowance"}).json()
    assert r["rating"] == 3
