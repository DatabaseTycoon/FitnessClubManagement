from dotenv import dotenv_values
from os import path
from database import Database

__env_path = path.join(path.dirname(__file__), ".env")
config = dotenv_values(__env_path)

if __name__ == "__main__":
    try:
        # Start database
        db = Database(
            db_name=config['DBNAME'],
            port=config['PORT'],
            user_name=config['UNAME'],
            password=config['PASSWORD']
        )
    except KeyError as ke:
        print(ke)
        print(".env may not have been configured properly.")
        exit(1)