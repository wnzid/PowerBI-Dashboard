# Improving the frontend

## Database setup

The backend uses a simple SQLite database stored as `Backend/users.db`.
To create the database and the required `users` table, run:

```bash
python Backend/init_db.py
```

This script creates the database file if it does not exist.
