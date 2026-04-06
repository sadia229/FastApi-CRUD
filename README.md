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
# FastApi-CRUD
