# Improving the frontend

## Database setup

The backend uses a simple SQLite database stored as `Backend/users.db`.
Both the application and helper scripts now determine the database path relative
to the `Backend` directory. This means you can start the Flask server from any
working directory without accidentally creating multiple database files.
To create the database and the required `users` table, run:

```bash
python Backend/init_db.py
```

This script creates the database file if it does not exist.
