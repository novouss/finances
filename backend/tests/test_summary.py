EXPECTED_KEYS = {
    "balance",
    "sum_income",
    "avg_income",
    "min_income",
    "max_income",
    "sum_expense",
    "avg_expense",
    "min_expense",
    "max_expense",
    "date_from",
    "date_to",
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
    assert s["date_from"] == "2026-08-01"
    assert s["date_to"] == "2026-08-12"


def test_summary_account_is_all_zeroes(client):
    _seed(client)
    s = client.get("/transactions/summary", params={"from_account": "Credits"}).json()
    assert set(s) == EXPECTED_KEYS
    assert all(v == 0 or v == "" for v in s.values())


def test_summary_date_window(client):
    _seed(client)
    s = client.get(
        "transactions/summary",
        params={
            "from_account": "Allowance",
            "date_from": "2026-08-03",
            "date_to": "2026-08-03",
        },
    ).json()
    assert s["sum_expense"] == 25
    assert s["sum_income"] == 0
    assert s["balance"] == -25
