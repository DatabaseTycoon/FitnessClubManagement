"""
Assorted database functions placed here until a better spot is found.
"""
import datetime

from database import Database


def init_db() -> Database:
    """
    Initialize the database using the env config

    :return: Database instance with config values
    """
    # Get config
    from dotenv import dotenv_values
    from os import path
    __env_path = path.join(path.dirname(path.dirname(path.dirname(__file__))), ".env")
    config = dotenv_values(__env_path)
    # Try to init database
    try:
        # Start database
        db = Database(
            db_name=config['DBNAME'],
            port=config['PORT'],
            user_name=config['UNAME'],
            password=config['PASSWORD']
        )
        return db
    except KeyError as ke:
        print(ke)
        print(".env may not have been configured properly.")
        exit(1)

if __name__ == "__main__":
    db = init_db()

    start_time = datetime.datetime(2024, 9, 12, 11)
    end_time = datetime.datetime(2024, 9, 12, 16)
    # get_available_rooms(db, start_time, end_time, ['bike'])
    book_class(db, 8, start_time, end_time, ['bike'])

    #
    # start_time = datetime.datetime(2024, 9, 13, 11)
    # end_time = datetime.datetime(2024, 9, 13, 16)
    # get_available_rooms(db, start_time, end_time)
    #
    # start_time = datetime.datetime(2024, 9, 12, 11)
    # end_time = datetime.datetime(2024, 9, 12, 16)
    # get_available_rooms(db, start_time, end_time)
    #
    # start_time = datetime.datetime(2024, 9, 12, 11)
    # end_time = datetime.datetime(2024, 9, 12, 16)
    # get_available_rooms(db, start_time, end_time, ['bike'])
    # _rooms = _get_rooms(db)
    # print(_rooms)
    # _rooms_filtered = _get_rooms(db, equipment_names=['a'])
