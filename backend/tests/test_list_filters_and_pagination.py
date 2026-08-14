import random


def test_list_filters_and_pagination(client):
    for i in range(15):
        client.post(
            "/transactions",
            json={
                "date": f"2026-08-{(i % 28) + 1:02d}",
                "from_account": random.choice(
                    ["Allowance", "Savings", "Funds", "Bills"]
                ),
                "to_account": random.choice(
                    ["Food", "Transport", "Fees", "Church", "Others", "Missing"]
                ),
                "amount": i + 1.0,
            },
        )

    print(client.get("/transactions").json())
    assert len(client.get("/transactions").json()) == 15

    page = client.get("/transactions", params={"limit": 5, "offset": 5})
    assert len(page.json()) == 5

    by_account = client.get("/transactions", params={"from_account": "check"})
    assert all(r["from_account"] == "checking" for r in by_account.json())
