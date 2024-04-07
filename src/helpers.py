from datetime import datetime

from src.db_api.database import Database


def get_option_input(options: list[str], title: str = "Options:", number_of_columns: int = 3):
    number_of_columns = min(number_of_columns, len(options))
    number_of_lines, remainder = divmod(len(options), number_of_columns)

    column_widths = []
    for i in range(number_of_columns):
        column_widths.append(max(len(max(options[i::number_of_columns], key=len)), 15) + 3)

    print('\n' + title)
    for i in range(0, number_of_lines * number_of_columns, number_of_columns):
        for j in range(number_of_columns):
            print(f'{i + 1 + j:>2}) {options[i + j]:<{column_widths[j]}}', end='')
        print('\n', end='')

    i = number_of_lines * number_of_columns
    for j in range(remainder):
        print(f'{i + 1 + j:>2}) {options[i + j]:<{column_widths[j]}}', end='')
    if remainder != 0:
        print('\n', end='')

    user_input = get_int_input(min=1, max=len(options))

    return user_input - 1


def get_int_input(prompt=" > ", min: int = None, max: int = None):
    while True:
        try:
            user_input = int(input(prompt))
            if (min is not None and user_input < min) or (max is not None and user_input > user_input > max):
                print(" Please enter a valid input.")
                continue
            break
        except ValueError:
            print(" Please enter a valid input.")

    return user_input


def get_date_input(prompt=" > "):
    while True:
        dob = input(prompt)
        try:
            date_of_birth = datetime.strptime(dob, "%Y/%m/%d")
            return date_of_birth.strftime("%Y-%m-%d")
        except ValueError:
            print("Incorrect date format. Please try again.")

def get_datetime_input(prompt=" > ") -> datetime:
    while True:
        dob = input(prompt+" (YYYY/MM/DD/HH): ")
        try:
            date = datetime.strptime(dob, "%Y/%m/%d/%H")
            return date
        except ValueError:
            print("Incorrect date format. Please try again.")


def get_all(db: Database, table_name: str) -> list[tuple[str]]:
    return db.select(['*'], table_name, {})
