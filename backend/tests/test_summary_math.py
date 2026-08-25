EXPECTED_KEYS = {
    "balance",
    "sum_income",
    "sum_expense",
    "avg_expense",
    "min_expense",
    "max_expense",
}


def _seed(client):
    client.post(
        "/transactions",
        json={
            "date": "2026-08-12",
            "from_account": "Salary",
            "to_account": "Allowance",
            "amount": 9999,
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


def test_summary_math(client):
    _seed(client)
    s = client.get("/transactions/summary", params={"from_account": "Allowance"}).json()
    assert set(s) == EXPECTED_KEYS
    assert s["sum_income"] == 9999
    assert s["sum_expense"] == 200
    assert s["balance"] == 9799
    assert s["avg_expense"] == 50.0
    assert s["min_expense"] == 25
    assert s["max_expense"] == 100
