# Mastercard Assignment

A RESTful API built with FastAPI for managing account operations. This application provides endpoints for creating, retrieving, and deleting accounts with proper validation and error handling.


This FastAPI application demonstrates a simple account management system with the following capabilities:
- Create new accounts with validation
- Retrieve account information
- Delete accounts
- Health check endpoint for monitoring
- Comprehensive error handling
- Full test coverage
- The application will be available at:
- **API**: `http://127.0.0.1:8000`
- **Interactive API docs**: `http://127.0.0.1:8000/docs`
- **Alternative docs**: `http://127.0.0.1:8000/redoc`

### Endpoints

| Method | Endpoint | Description | Status Codes |
|--------|----------|-------------|--------------|
| GET | `/healthz` | Health check | 200 |
| GET | `/accounts/{account_id}` | Get account by ID | 200, 404 |
| PUT | `/accounts/{account_id}` | Create new account | 201, 409 |
| DELETE | `/accounts/{account_id}` | Delete account | 200, 404 |


## Docker Usage

### Build Image

```bash
docker build -t mastercard-api .
```

### Run Container

```bash
docker run -d -p 8000:8000 --name mastercard-fastapi mastercard-api
```

## Uni tests

================================================================================================= tests coverage ==================================================================================================
________________________________________________________________________________ coverage: platform darwin, python 3.12.9-final-0 _________________________________________________________________________________

Name      Stmts   Miss  Cover   Missing
---------------------------------------
main.py      45      0   100%
---------------------------------------
TOTAL        45      0   100%
Coverage HTML written to dir htmlcov
Required test coverage of 90% reached. Total coverage: 100.00%
================================================================================================ 9 passed in 1.55s ===============================================================================================


Commands

```bash
pytest test_main.py -v
```

Coverage
```bash
pytest test_main.py --cov=main --cov-report=term-missing --cov-report=html --cov-fail-under=90 -v
```
