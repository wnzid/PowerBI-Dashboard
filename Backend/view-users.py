import sqlite3
from cryptography.fernet import Fernet
import os

FERNET_KEY = os.getenv("FERNET_KEY")
if not FERNET_KEY:
    FERNET_KEY = Fernet.generate_key().decode()
cipher = Fernet(FERNET_KEY.encode())

def decrypt_pw(token: str) -> str:
    try:
        return cipher.decrypt(token.encode()).decode()
    except Exception:
        return token

# Connect to the SQLite database
conn = sqlite3.connect("users.db")
c = conn.cursor()

# Fetch all users
c.execute("SELECT * FROM users")
users = c.fetchall()

# Print users
print("All registered users:")
for user in users:
    user_list = list(user)
    if len(user_list) > 2:
        user_list[2] = decrypt_pw(user_list[2])
    print(tuple(user_list))

conn.close()
