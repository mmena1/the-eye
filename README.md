# The Eye

Service that collects user web interactions as events in `json` format from external applications. These applications can send events to the Eye as POST requests to the `/events` endpoint which are then validated and stored in the database using an async queue by django-rq.

Example of valid events:

```json
{
  "session_id": "e2085be5-9137-4e4e-80b5-f1ffddc25423",
  "category": "page interaction",
  "name": "pageview",
  "data": {
    "host": "www.consumeraffairs.com",
    "path": "/",
  },
  "timestamp": "2021-01-01 09:15:27.243860"
}

{
  "session_id": "e2085be5-9137-4e4e-80b5-f1ffddc25423",
  "category": "page interaction",
  "name": "cta click",
  "data": {
    "host": "www.consumeraffairs.com",
    "path": "/",
    "element": "chat bubble"
  },
  "timestamp": "2021-01-01 09:15:27.243860"
}

{
  "session_id": "e2085be5-9137-4e4e-80b5-f1ffddc25423",
  "category": "form interaction",
  "name": "submit",
  "data": {
    "host": "www.consumeraffairs.com",
    "path": "/",
    "form": {
      "first_name": "John",
      "last_name": "Doe"
    }
  },
  "timestamp": "2021-01-01 09:15:27.243860"
}
```

There are 2 ways to run it: with Docker or with a local server. For demo purposes, the local server uses SQLite while the Docker approach uses PostgreSQL. But it can easily be changed on the settings.

## Get Started - Docker

1. **Requirements:**

    Copy the `.env.example` file to `.env` and edit it to populate its variables.
    ```bash
    cp .env.example .env
    ```

    Run the following command to generate a random secret key and add it to your `.env` file.
    ```bash
    base64 /dev/urandom | head -c50

    # .env
    DJANGO_SECRET_KEY=<generated_key>
    ```

    Add postgres variables to your `.env` file:

    ```bash
    cat <<EOT >> .env
    POSTGRES_USER=postgres
    POSTGRES_PASSWORD=postgres
    POSTGRES_HOST=db
    POSTGRES_PORT=5432
    EOT
    ```

    You can set different values or use these as default.

1. **Start the app**

    Make sure you have [docker-compose](https://docs.docker.com/compose/install/) installed on your system. Then just run:

    ```
    docker-compose up
    ```

    This will start the following containers:
    - Redis
    - Postgres
    - Django RQ
    - Django app

    After it finishes configuring everything you can make `curl` requests to the endpoints as described in the [Using the service](#using-the-service) section.
## Get Started - Local Server

1. **Requirements:**

    - Python 3.9
    - Unix compatible environment (Linux/OSX)
    - A running Redis server instance. The easiest way is to run through the official docker image:
      ```
      docker run --rm -p 6379:6379 -d redis:latest
      ```

1. **Initialize a python virtual environment:**

    ```bash
    python3 -m venv venv
    source venv/bin/activate
    ```

1. **Install the project dependencies:**

    ```bash
    pip install -r requirements.txt
    ```

1. **Initialize the project:**

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
The service exposes two endpoints to query and register events.

A few things to consider:
- Timestamps can be either ISO format or `%Y-%m-%d %H:%M:%S.%f`, which is basically the same except a space instead of `T`.
  - `2022-04-11T01:08:01.407119` (ISO)
  - `2022-04-11 01:08:01.407119`
- At the moment, there are only 3 types of allowed payload data:
  - category: `page_interaction` and name: `page_view`:
    ```json
    "data": {
      "host": "www.consumeraffairs.com",
      "path": "/",
    },
    ```
  - category: `page_interaction` and name: `cta_click`:
    ```json
    "data": {
      "host": "www.consumeraffairs.com",
      "path": "/",
      "element": "chat bubble"
    },
    ```
  - category: `form_interaction` and name: `submit` (form data can be any valid `json`):
    ```json
    "data": {
      "host": "www.consumeraffairs.com",
      "path": "/",
      "form": {
        "first_name": "John",
        "last_name": "Doe"
      }
    },
    ```
  - Any other value will result in a validation error.
- If this service is accessed using a browser, the browsable API feature will kick in and the default html template will render.

### **Register an event**
Make a POST request to `/events`:
```
curl -X POST http://localhost:8000/events \
    -H "Content-Type: application/json"
    -d '{"session_id": "123", "category": "page_interaction", "name": "page_view", "data": {"host": "www.consumeraffairs.com", "path": "/"}, "timestamp": "2022-01-01 00:00:00.000000"}' \
```
This should return a 201 response. You can inspect the RQ worker terminal prompt for details on the execution to see if it saved successfully or an error occurred.

### **Query existing events**
Make a GET request to `/events`:
```
curl http://localhost:8000/events
```
This should return a list of all registered events in JSON format and sorted by timestamp (DESC).

NOTE: This endpoint is paginated, meaning that you will only see 10 records at a time (which can be configured on the Django settings). In order to access more records you need to pass a `page=<number>` to the query params:
```
curl http://localhost:8000/events?page=2
```
There are 3 different query params you can pass to filter the data by session, category or timestamp range. Also any combination of the 3 is supported:
```
curl http://localhost:8000/events?session_id=abc123
curl http://localhost:8000/events?category=name
curl http://localhost:8000/events?start_time=2022-01-01&end_time=2022-02-01
curl http://localhost:8000/events?session_id=abc123&category=name&start_time=2022-01-01&end_time=2022-02-01
```

### Debugging errors
The non-docker approach uses a file logger that contains the logs of the service. You can inspect the `the_eye/logs/server.log` file for errors that have been raised along with the request payload.

As for the docker approach, you can use the built-in docker logs command to inspect the logs of a running container:

```bash
docker logs consumer-affairs-test-django_rq-1 --tail 50 --follow
```
This will show the last 50 lines of the Django RQ logs and will keep the prompt open to listen to new log data.

## Unit Tests
Run the following command to run all unit tests:
```
python manage.py test
```
## Distribute the service
You can generate a `.tar.gz` file with the service code:
  
  ```bash
  python setup.py sdist
  ```

Then you can install it on another Django project by running the following command:

```bash
pip install /path/to/django-the-eye-0.1.tar.gz
```
NOTE: An easier way would be to upload the service to the Python Package Index (PyPI) or to a private repository manager (such as [Artifactory](https://jfrog.com/artifactory/)) and then add it to your `requirements.txt` file.