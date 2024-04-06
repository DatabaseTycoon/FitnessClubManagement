from db_api.database import Database
from dotenv import dotenv_values
from os import path
from helpers import *
from member import Member
from staff import Staff
from admin import Admin
from trainer import Trainer

__env_path = path.join(path.dirname(path.dirname(__file__)), ".env")
config = dotenv_values(__env_path)


def start_screen(db: Database):
    print("\n" * 40)
    option = get_option_input(["Login", "Register"], "Welcome to Fitness Club Management App")

    if option == 0:
        user_type = get_option_input(["Member Login", "Staff Login"], "Select Login Type:")
        print()
        if user_type == 0:
            print("Enter your member id to login.")
            member_id = get_int_input("MemberID: ")
            member_infos = Member.get_member_info(db, member_id)

            while len(member_infos) == 0:
                print("MemberID not found. Try again.")
                member_id = get_int_input("MemberID: ")
                member_infos = Member.get_member_info(db, member_id)

            member = Member(member_infos[0][0], db)
            member.show_main_menu()
        else:
            print("Enter your staff id to login.")
            staff_id = get_int_input("StaffID: ")

            staff_info = Staff.get_staff_info(db, staff_id)
            while staff_info is None:
                print("StaffID not found. Try again.")
                staff_id = get_int_input("StaffID: ")
                staff_info = Staff.get_staff_info(db, staff_id)

            if staff_info[0] == "Admin":
                admin = Admin(staff_info[1], staff_id, db)
                admin.show_main_menu()
            else:
                trainer = Trainer(staff_info[1], staff_id, db)
                trainer.show_main_menu()

            print("StaffID: ", staff_id)
    else:
        Member.register(db)


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

    start_screen(db)
