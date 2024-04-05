from dotenv import dotenv_values
from os import path
from database import Database

__env_path = path.join(path.dirname(path.dirname(path.dirname(__file__))), ".env")
config = dotenv_values(__env_path)


def main(db: Database):

    ins_res = db.insert_into("members", rows=["name"], values=["Hello1"])
    ins_res = db.insert_into("members", rows=["name"], values=["Hello2"])
    ins_res = db.insert_into("members", rows=["name"], values=["Hello3"])
    ins_res = db.insert_into("members", rows=["name"], values=["Hello4"])
    ins_res = db.insert_into("members", rows=["name"], values=["Hello5"])
    ins_res = db.insert_into("members", rows=["name"], values=["Hello5"])
    ins_res = db.insert_into("members", rows=["name"], values=["Hello5"])
    ins_res = db.insert_into("members", rows=["name"], values=["Hello5"])

    del_res = db.delete_from("members", {"operation": "=", "rowA": "name", "rowB": "Hello5"})

    sel_res = db.select(["*"], "members", select_options={
        "WHERE": {"operation": "<=", "rowA": "memberid", "rowB": "2"}
    })

    sel_res_or = db.select_with_or(["*"], "members", 
                                   {"operation": "<=", "rowA": "memberid", "rowB": "2"},
                                   {"operation": ">=", "rowA": "memberid", "rowB": "3"},
                                   {"operation": "=", "rowA": "memberid", "rowB": "4"})

    print(sel_res, sel_res_or, del_res, ins_res)
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