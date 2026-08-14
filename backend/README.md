## How to run the backend

```bash
cd backend
uv sync
uv run backend
```

## How to curl to the backend

```bash
curl http://localhost:8000/health
curl -X POST http://localhost:8000/transactions -H 'Content-Type: application/json' -d '{"from_account":"Allowance","to_account":"Savings","amount":100}'
curl -X POST http://localhost:8000/transactions -H 'Content-Type: application/json' -d '{"from_account":"Allowance","to_account":"Food","amount":90,"description":"Rice"}'
curl -X PATCH http://localhost:8000/transactions/2 -H 'Content-Type:application/json' -d '{"description":"Rice Meal"}'
curl http://localhost:8000/transactions/2
curl http://localhost:8000/transactions
curl -X DELETE http://localhost:8000/transactions/1
curl -X DELETE http://localhost:8000/transactions/2
```
