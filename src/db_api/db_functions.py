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


def get_all(db: Database, table_name: str) -> list[tuple[str]]:
    return db.select(['*'], table_name, {})


def _get_bookings(db, time_start, time_end) -> set[tuple[str]]:
    def is_before(s1, e1, sTest):
        """
        :param s1: The given start time
        :param e1: The given end time
        :param sTest: The start time to compare against
        :return: If s1, e1 before the reference sTest, then return True, else False.
        """
        return s1 < sTest and e1 < sTest

    def is_after(s1, e1, eTest):
        """
        :param s1: The given start time
        :param e1: The given end time
        :param eTest: The end time to compare against
        :return: If s1, e1 after the reference eTest, then return True, else False.
        """
        return s1 > eTest and e1 > eTest

    START_INDEX = 2
    END_INDEX = 3
    ROOM_INDEX = 1
    all_classes = get_all(db, 'gymclass')
    bookings = []
    for cls in all_classes:
        # If either start/end times fall within a booked class time, add to bookings list
        if not (is_before(time_start, time_end, cls[START_INDEX]) or is_after(time_start, time_end, cls[END_INDEX])):
            bookings.append((cls[ROOM_INDEX],))
    return set(bookings)


def _get_equipment_rooms(db, equipment_names) -> set[tuple[str]]:
    NAME_INDEX = 3
    ROOM_INDEX = 1
    all_equipment = get_all(db, 'equipment')
    print(all_equipment)
    equipment_rooms = set()
    for equipment in all_equipment:
        # If there exists a name in the given list which matches the current equipment name,
        #   save the room the equipment is in. Note: Capacity/Counts are considered out of scope atm
        if (name for name in equipment_names if name == equipment[NAME_INDEX]):
            equipment_rooms.add((equipment[ROOM_INDEX],))
    return equipment_rooms


def _get_available_rooms(db: Database,
                        time_start: datetime.datetime,
                        time_end: datetime.datetime,
                        equipment_names: list[str] = None) -> set[tuple[str]]:
    """
    Return view of booked rooms at a particular time.

    :param time_start:
    :param time_end:
    :param db:
    :return: Room IDs of rooms available for bookings, which have the equipment specified (if applicable)
    """
    # Filter out booked rooms from all rooms
    all_rooms = set(get_all(db, 'room'))  # Returns IDs, should be unique
    # Find which classes correspond to bookings at given times
    all_bookings = _get_bookings(db, time_start, time_end)
    # Find rooms with matching equipment needs (no needs, all rooms accepted)
    all_equipment_rooms = all_rooms if not equipment_names else _get_equipment_rooms(db, equipment_names)

    # Return query result by applying filters (with intersection + subtraction)
    return all_equipment_rooms.intersection(all_rooms - all_bookings)


def book_class(db: Database, class_capacity: int, start_time, end_time, equipment_names: list[str] = None):
    available_rooms = _get_available_rooms(db, start_time, end_time, equipment_names)

    if not available_rooms:
        print('No rooms available for booking')
        return

    # Create a new class
    db.insert_into('gymclass',
                   [available_rooms.pop()[0], start_time, end_time, class_capacity],
                   ['roomid', 'startdate', 'enddate', 'capacity'])

    print('Booked class, new class list:')
    # TODO: improve printing
    print(get_all(db, 'gymclass'))

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
