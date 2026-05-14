# Deployment and PostgreSQL Setup

## PostgreSQL connection

1. Create a single `.env` file in the project root.
2. Update the values to match your PostgreSQL instance.

Example `.env` values:
```text
SECRET_KEY=your-secret-key
DEBUG=False
ALLOWED_HOSTS=your-domain.com
CORS_ALLOW_ALL_ORIGINS=False
CORS_ALLOWED_ORIGINS=http://localhost:3000,http://127.0.0.1:3000
DB_NAME=opportunityhub
DB_USER=postgres
DB_PASSWORD=19alo82
DB_HOST=127.0.0.1
DB_PORT=5432
```

3. Install requirements:
```bash
pip install -r requirements.txt
```

4. Apply migrations:
```bash
python manage.py makemigrations
python manage.py migrate
```

5. Create a superuser if needed:
```bash
python manage.py createsuperuser
```

## Recommended free hosting options

### Better free option
- **Railway** – good for standard Django + PostgreSQL projects. It supports persistent Postgres databases and has a generous free tier.
- **Fly.io** – also solid if you want a lightweight always-on app with PostgreSQL.

### Use with caution
- **Render free** is convenient but the app will sleep after inactivity. It is okay for prototypes, but not for production or demos that must be instantly available.

### Recommended approach
- Use **Railway** for deployment and connect a managed PostgreSQL database.
- Keep `DEBUG=False` in production and set `ALLOWED_HOSTS`.
- Use `python-decouple` environment variables from the `.env` file.

## Production checklist

- Set `DEBUG=False`
- Add your domain or host to `ALLOWED_HOSTS`
- Use a secure `SECRET_KEY`
- Enable HTTPS on the hosting platform
- Run migrations after deployment
- Use a managed PostgreSQL database and keep credentials secure
