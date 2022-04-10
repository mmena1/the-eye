# The Eye
Service that collects user web interactions from applications.

## Get Started

**Prerequisites:**

- Python 3.9
- Unix compatible environment (Linux/OSX)
- A running Redis server instance. The easiest way is to run through the official docker image:
  ```
  docker run --rm -p 6379:6379 -d redis:latest
  ```

Initialize a python virtual environment:

```bash
python3 -m venv venv
source venv/bin/activate
```

**Install the project dependencies:**

```bash
pip install -r requirements.txt
```

**Initialize the project:**

Copy the `.env.example` file to `.env` and edit it to populate its variables.
```bash
cp .env.example .env
```

Run the following command to generate a random secret key and add it to your `.env` file.
```bash
python -c "from django.core.management.utils import get_random_secret_key;print(get_random_secret_key())"

# .env
DJANGO_SECRET_KEY=<generated_key>
```

Run DB migrations:

```bash
python manage.py migrate
```

Start the Django server:
```
python manage.py runserver
```
Start the RQ worker on another terminal prompt:
```
python manage.py rqworker
```

## Using the service
There are two endpoints you can interact with the service:
### Register an event
Make a POST request to `/events`:
```
curl -X POST http://localhost:8000/events \
    -H "Content-Type: application/json"
    -d '{"session_id": "123", "category": "page_interaction", "name": "page_view", "data": {"host": "www.consumeraffairs.com", "path": "/"}, "timestamp": "2022-01-01 00:00:00.000000"}' \
```
This should return a 201 response. You can inspect the RQ worker terminal prompt for details on the execution to see if it saved successfully or an error occurred.

### Query existing events
Make a GET request to `/events`:
```
curl http://localhost:8000/events
```
This should return a list of all registered events in JSON format.


## Unit Tests
Run the following command to run all unit tests:
```
python manage.py test
```