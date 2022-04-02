# The Eye
Service that collects events from applications

## Requirements
- Python 3.9

## Get Started

**Prerequisites:**

- Python 3.9

Initialize a python virtual environment:

```bash
python3 -m venv venv
source ./venv/bin/activate
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