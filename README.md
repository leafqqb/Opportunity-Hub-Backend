# Opportunity Hub Backend

A Django REST Framework backend for Opportunity Hub, a platform for students and companies to connect over internships, jobs, scholarships, and other career opportunities.

## Features

- Secure student and company registration/login
- Token-based authentication
- User profile management
- Opportunity browsing, creation, update, and deletion
- Student bookmarks for saved opportunities
- PostgreSQL-ready database configuration
- Production-ready settings for deployment with `whitenoise`

## Tech stack

- Python 3.13
- Django 6.x
- Django REST Framework
- PostgreSQL
- `rest_framework.authtoken` for token auth
- `python-decouple` for environment configuration
- `django-cors-headers` for cross-origin support
- `whitenoise` for static file serving

## Quick start

1. Clone the repo:
   ```bash
   git clone https://github.com/leafqqb/Opportunity-Hub-Backend.git
   cd "Opportunity Hub"
   ```

2. Create and activate a virtual environment:
   ```bash
   python -m venv .venv
   .\.venv\Scripts\activate
   ```

3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

4. Create a `.env` file in the project root and add your settings.
   Example:
   ```text
   SECRET_KEY=your-secret-key
   DEBUG=True
   ALLOWED_HOSTS=localhost,127.0.0.1
   CORS_ALLOW_ALL_ORIGINS=False
   CORS_ALLOWED_ORIGINS=http://localhost:3000,http://127.0.0.1:3000
   DB_NAME=opportunityhub
   DB_USER=postgres
   DB_PASSWORD=your-password
   DB_HOST=127.0.0.1
   DB_PORT=5432
   ```

5. Run migrations:
   ```bash
   python manage.py makemigrations
   python manage.py migrate
   ```

6. Start the development server:
   ```bash
   python manage.py runserver
   ```

7. Open the API at:
   ```text
   http://localhost:8000/api/
   ```

## Testing

Run the API tests with:
```bash
python manage.py test api
```

## API documentation

See `API_GUIDE.md` for detailed endpoint usage, including:

- Authentication and token flow
- Profile endpoints
- Opportunity management
- Bookmark creation, listing, and removal

## Deployment

For production deployment, see `DEPLOYMENT.md`.

Key recommendations:

- Keep `DEBUG=False`
- Use a secure `SECRET_KEY`
- Configure `ALLOWED_HOSTS`
- Deploy with PostgreSQL
- Run migrations after deploying
- Use `python-decouple` to manage environment variables

## Notes

- The backend uses `TokenAuthentication` for protected endpoints.
- Student users can bookmark opportunities using `/api/bookmarks/`.
- Company users can create and manage opportunities.
