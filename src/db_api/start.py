from dotenv import dotenv_values
from os import path
from database import Database

__env_path = path.join(path.dirname(path.dirname(path.dirname(__file__))), ".env")
config = dotenv_values(__env_path)


def main(db: Database):

    res = db.select(["*"], "members", select_options={
        "WHERE": {"operation": "<=", "rowA": "memberid", "rowB": "2"}
    })

    print(res)
    exit(0)


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
    
    main(db)