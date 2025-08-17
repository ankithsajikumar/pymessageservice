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

---

## Authentication

- **SSO OAuth2:**  
  - The application uses an external SSO OAuth2 provider for authentication.
  - Users are redirected to the SSO login page (`/admin/login/`), and after successful authentication, are redirected back to `/auth/callback/`.
  - The backend exchanges the authorization code for an access token and logs in the user.
  - The access token is used internally by the backend to fetch user info and manage the session.

  ```
  # Example: Logging in via SSO
  1. Visit /admin/login/
  2. Authenticate with the SSO provider
  3. On success, you are redirected and logged in to the Django admin
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

## TODO

- [ ] Implement BFF (Backend For Frontend) pattern to securely expose authentication/session info for frontend apps.
    - The backend should handle all OAuth2 flows and session management.
    - Frontend apps should interact only with the Django backend (BFF), not directly with the SSO provider.
    - Provide endpoints for the frontend to fetch user info and perform authenticated actions without exposing access tokens to the browser.
- [ ] Add API endpoints for message CRUD operations.
- [ ] Improve error handling and logging.
- [ ] Add unit and integration tests.
- [ ] Enhance documentation for API usage and authentication flows.

---

## BFF Pattern for Frontend Apps

To securely integrate frontend applications (React, Angular, etc.):

- The Django backend acts as a **Backend For Frontend (BFF)**, handling all authentication and session logic.
- The frontend communicates only with the Django backend via REST APIs.
- The backend manages OAuth2 tokens and user sessions, never exposing sensitive tokens to the frontend.
- The frontend can fetch user info or perform actions by calling protected endpoints on the backend, which proxies requests as needed.

This approach improves security and simplifies frontend logic by centralizing authentication and session management in the backend.

---

## License

MIT License