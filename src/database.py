import psycopg

class Database():

    def __init__(self, db_name: str, user_name: str, password: str, port: str) -> None:
        try:
            self.__connection = psycopg.connect(
                f"dbname={db_name} user={user_name} password={password} port={port}"
            )

        except psycopg.OperationalError as e:
            print(e)
            exit(1)