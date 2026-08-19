import random


def test_summary(client):

    income = 9999
    sum_expense = 0
    min_expense = income
    max_expense = 0
    count_expense = 15

    client.post(
        "/transactions",
        json={
            "date": "2026-08-12",
            "from_account": "Salary",
            "to_account": "Allowance",
            "amount": income,
        },
    )

    for i in range(count_expense):
        expense = random.randint(1, 100)

        sum_expense = sum_expense + expense
        min_expense = min(min_expense, expense)
        max_expense = max(max_expense, expense)

        client.post(
            "/transactions",
            json={
                "date": f"2026-08-{(i % 28) + 1:02d}",
                "from_account": "Allowance",
                "to_account": "Food",
                "amount": expense,
            },
        )

    avg_expense = sum_expense / count_expense

    summary = client.get(
        "/transactions/summary", params={"from_account": "Allowance"}
    ).json()

    assert summary["balance"] == income - sum_expense
    assert summary["sum_income"] == income
    assert summary["sum_expense"] == sum_expense
    assert summary["avg_expense"] == avg_expense
    assert summary["min_expense"] == min_expense
    assert summary["max_expense"] == max_expense
