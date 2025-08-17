# MessageBridge (PyMessageService)

A Django-based messaging and smart device service providing APIs for polling messages and smart home fulfillment, with authentication via OAuth2.

---

## Features

- Custom user and message models
- Poll unread messages and mark as read
- Smart home fulfillment endpoint (Google Smart Home)
- OAuth2 authentication support
- Admin interface
- Logging for error tracking

---

## Getting Started

### 1. Clone the repository

```sh
git clone https://github.com/ankithsajikumar/pymessageservice.git
cd pymessageservice
```

### 2. Set up a virtual environment

```sh
python -m venv venv
source venv/bin/activate
```

### 3. Install requirements

```sh
pip install -r requirements.txt
```

### 4. Apply migrations

```sh
python manage.py migrate
```

### 5. Create a superuser

```sh
python manage.py createsuperuser
```

### 6. Run the development server

```sh
python manage.py runserver
```

### MISC: Deactivate venv

```sh
deactivate
```

### MISC: Collect dependencies

```sh
pip freeze > requirements.txt
```

---

## API Endpoints

- **Home Page:**  
  - `GET /home/` — Landing page

- **Poll Messages:**  
  - `POST /api/poll-messages/` — Poll unread messages and mark messages as read  
    ```sh
    curl -X POST https://domain/api/poll-messages/ \
      -H "Authorization: Bearer <access_token>" \
      -H "Content-Type: application/json" \
      -d '{"messagesRead": ["uuid1", "uuid2"]}'
    ```
    - Returns all unread messages and marks the provided message IDs as read.

- **Smart Home Fulfillment:**  
  - `POST /smarthome/fulfillment/` — Handles smart home intents (SYNC, QUERY, EXECUTE, DISCONNECT)  
    - Requires appropriate permissions and payload structure.

- **OAuth2:**  
  - `/o/` — OAuth2 endpoints (see [django-oauth-toolkit docs](https://django-oauth-toolkit.readthedocs.io/en/latest/))

---

## Authentication

- **OAuth2:**  
  Obtain a token via `/o/token/` and use it in the `Authorization` header:  
  ```
  Authorization: Bearer <access_token>
  ```

---

## Useful Django Commands

- Run development server:  
  `python manage.py runserver`
- Make migrations:  
  `python manage.py makemigrations`
- Apply migrations:  
  `python manage.py migrate`
- Create superuser:  
  `python manage.py createsuperuser`
- Open Django shell:  
  `python manage.py shell`
- Collect static files:  
  `python manage.py collectstatic`

---

## Project Structure

```
pymessageservice/
├── manage.py
├── requirements.txt
├── README.md
├── messagesApp/
│   ├── models.py
│   ├── views.py
│   ├── admin.py
│   └── ...
├── smartDevices/
│   ├── models.py
│   ├── admin.py
│   └── ...
├── smartIntents/
│   ├── views.py
│   ├── services.py
│   └── ...
├── users/
│   ├── models.py
│   ├── admin.py
│   └── ...
├── lobby/
│   ├── views.py
│   └── ...
└── pymessageservice/
    ├── settings.py
    ├── urls.py
    └── ...
```

---

## License

MIT License