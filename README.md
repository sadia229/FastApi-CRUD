# Clean Architecture FastAPI CRUD

This project provides a production-leaning FastAPI CRUD example using clean architecture layers:

- `domain`: business entities and repository contracts
- `application`: service/use-case logic
- `infrastructure`: database and repository implementations
- `presentation`: FastAPI routes and dependency wiring

## Run

```bash
python3 -m uvicorn presentation.main:app --app-dir src --reload
```

## Database

By default the app uses SQLite:

```env
DATABASE_URL=sqlite+aiosqlite:///./app.db
```

You can switch to PostgreSQL later with:

```env
DATABASE_URL=postgresql+asyncpg://user:password@localhost:5432/app_db
```

## Deploy To Render

This repo includes [render.yaml](/Users/macbookpro13inch/Desktop/fastapi-project/render.yaml), which defines:

- one Python web service
- one Render Postgres database
- automatic `DATABASE_URL` injection from the database into the web service

Deploy steps:

```bash
git add .
git commit -m "Add Render deployment config"
git push
```

Then in Render:

```text
New + -> Blueprint -> connect your GitHub repo -> apply render.yaml
```

The app starts with:

```bash
uvicorn presentation.main:app --app-dir src --host 0.0.0.0 --port $PORT
```

Note:

- Render provides a standard Postgres connection string like `postgresql://...`
- this app automatically converts it to `postgresql+asyncpg://...` for SQLAlchemy async
