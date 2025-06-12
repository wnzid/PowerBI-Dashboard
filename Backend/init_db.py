import os
import sys

# Ensure the repository root is on the Python path
sys.path.append(os.path.dirname(os.path.dirname(__file__)))

from db import init_db, DB_PATH

if __name__ == "__main__":
    init_db()
    print(f"Database initialized at {DB_PATH}.")
