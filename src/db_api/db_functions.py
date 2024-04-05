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


def _get_rooms(db: Database, equipment_names: list[str] = None):
    """
    Get all rooms in the database

    :param db:
    :return:
    """
    if equipment_names is None:
        return db.select(['roomID'], 'room', {})
    # TODO: test this
    equipment_name_key = f"({0})".format(", ".join(equipment_names))


    return db.select(['roomID'], 'equipment', {"WHERE": {"operation": "IN",
                                                         "rowA": 'equipmentName',
                                                         "rowB": equipment_name_key}})


def view_available_rooms(db: Database, time_start: datetime.datetime, time_end: datetime.datetime) -> None:
    """
    Return view of booked rooms at a particular time.

    :param time_start:
    :param time_end:
    :param db:
    :return:
    """


if __name__ == "__main__":
    db = init_db()
    # _rooms = _get_rooms(db)
    # print(_rooms)
    _rooms_filtered = _get_rooms(db, equipment_names=['a'])
