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


def startScreen(db: Database):
    print("\n" * 40)
    option = get_option_input(["Login", "Register"], "Welcome to Fitness Club Management App")

    if option == 0:
        userType = get_option_input(["Member Login", "Staff Login"], "Select Login Type:")
        print()
        if userType == 0:
            print("Enter your member id to login.")
            member_id = get_int_input("MemberID: ")
            member_infos = Member.get_member_info(db, member_id)

            while len(member_infos) == 0:
                print("MemberID not found. Try again.")
                member_id = get_int_input("MemberID: ")
                member_infos = Member.get_member_info(db, member_id)

            member = Member(member_infos[0][0])
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
                admin = Admin(staff_info[1], staff_id)
                admin.show_main_menu()
            else:
                trainer = Trainer(staff_info[1], staff_id)
                trainer.show_main_menu()

            print("StaffID: ", staff_id)
    else:
        Member.register(db)

    # equipment_data = db.select(["*"], "equipment", select_options={
    #     "WHERE": {"operation": "<", "rowA": "equipmentId", "rowB": "roomId"}
    # })
    #
    # while (True):
    #     print("\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n")
    #
    #     # Print equipment information in a tabular format
    #     print("\n\t\tEQUIPMENT MAINTENANCE MONITORING\n")
    #     print("{:<10} {:<15} {:<30} {:<10}".format("Equip ID", "Status", "Equipment Name", "Room ID"))
    #     print("{:<10} {:<15} {:<30} {:<10}".format("--------", "------", "--------------", "-------"))
    #     for equipment_id, room_id, status, equipment_name in equipment_data:
    #         print("{:<10} {:<15} {:<30} {:<10}".format(equipment_id, status, equipment_name, room_id))
    #
    #     # Print options
    #     # print("\nOptions:")
    #     # print("0) Quit", "\t1) Sort by room", "\t2) Sort by status",
    #     #       "\n3) Filter for Working", "\t4) Filter for Maintenance", "\t5) Filter for Out of Order")
    #
    #     o_list = ["Quit", "Sort by room", "Sort by status", "Filter for Working", "Filter for Maintenance",
    #               "Filter for Out of Order", "ExtraOption1", "ExtraLooooooooooooooooooooooooooooongOption1"]
    #     option = get_option_input(o_list)
    #
    #     if option == '0':
    #         break
    #     if option == '1':
    #         equipment_data.sort(key=lambda e: e[1])
    #     elif option == '2':
    #         equipment_data.sort(key=lambda e: e[2])
    #     elif option == '3':
    #         equipment_data = list(filter(lambda e: e[2] == 'Working', equipment_data))
    #     elif option == '4':
    #         equipment_data = list(filter(lambda e: e[2] == 'Maintenance', equipment_data))
    #     elif option == '5':
    #         equipment_data = list(filter(lambda e: e[2] == 'Out of Order', equipment_data))
    #     else:
    #         pass


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

    startScreen(db)
