# Improving the frontend

## Database setup

The project stores user information in a SQLite database located at
`Backend/users.db`.  A new `db.py` module centralises the database connection
logic so both the API in `app.py` and the web application in
`Backend/app.py` use the same file.  This means you can start the server from
any directory without creating multiple database copies.
To create the database and the required `users` table, run:

```bash
python Backend/init_db.py
```

This script creates the database file if it does not exist.
