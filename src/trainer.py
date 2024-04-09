import time

from helpers import *
from db_api.database import Database


class Trainer:
    def __init__(self, trainer_id: int, staff_id: int, db: Database):
        self.trainer_id = trainer_id
        self.staff_id = staff_id
        self.db = db

    def show_main_menu(self):
        while True:
            print("\n" * 50)
            main_menu_options = ["View Member Profile", "Schedule teaching", "View Schedule", "Cancel teaching", "Back"]
            selected_option = get_option_input(main_menu_options, "Trainer Menu", 3)

            if selected_option == 0:
                print("Selected: View Member Profile")
                self.view_profile()
            elif selected_option == 1:
                print("Selected: Schedule teaching")
                self.teach_class()
            elif selected_option == 2:
                print("Selected: View Schedule")
                self.see_ran_classes()
            elif selected_option == 3:
                print("Selected: Cancel teaching")
                self.drop_ran_class()
            elif selected_option == 4:
                return

    def view_profile(self) -> None:
        members = self.db.select(['memberinfo', 'personalinfoid'], 'memberinfo', {})
        p_info = self.db.select(['personalinfoid', 'contactid'], 'personalinfo', {})
        c_info = self.db.select(['contactid', 'firstname', 'lastname', 'email'], 'contactinfo', {})

        print("\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n")
        print("\n\t\tMEMBERS LIST\n")

        print("{:<10} {:<20} {:<20} {:<10}".format("MemberID", "First Name", "Last Name", "Email"))
        for member in members:
            member_pinfo = list(filter(lambda personal: personal[0] == member[1], p_info))[0]
            member_contact = list(filter(lambda contact: contact[0] == member_pinfo[1], c_info))[0]
            print("{:<10} {:<20} {:<20} {:<10}".format(member[0], member_contact[1], member_contact[2],
                                                       member_contact[3]))

        # Ask for input after member list display
        _id = None
        member_ids = [member[0] for member in members]
        while _id not in member_ids:
            _id = int(input(" > select member id to view: "))

        # reselect specific member (get first id match, in theory only one):
        g_info = self.db.select_with_or(['*'], 'fitnessgoal',
                                        {'operation': '=', 'rowA': 'memberid', 'rowB': str(_id)})

        member_pinfo = list(filter(lambda personal: personal[0] == member[1], p_info))[0]
        member_contact = list(filter(lambda contact: contact[0] == member_pinfo[1], c_info))[0]
        print("\n" * 50)
        print("\n\t\tSELECTED MEMBER INFO\n")
        print("Selected member {}, {}'s goals:".format(member_contact[1], member_contact[2]))
        print("{:<10} {:<20} {:<20} {:<10}".format("Type", "Description", "Acheived", "Target"))
        for goal in g_info:
            type_ = goal[1]
            desc = goal[2]
            acheived = "yes" if goal[3] else "no"
            target = str(goal[4])

            print("{:<10} {:<20} {:<20} {:<10}".format(type_, desc, acheived, target))

        input("\nPress enter to continue > ")

    def teach_class(self):
        # Step 1: Show teacherless classes
        runs = self.db.select(['classid'], 'runs', {})
        ran_classes_ids = [run[0] for run in runs]  # unpack tuple as str
        classes = self.db.select(["*"], 'gymclass', {})
        non_ran_classes = [cls for cls in classes if cls[0] not in ran_classes_ids]

        print("\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n")
        print("\n\t\tCLASS LIST (unassigned only)\n")
        print("{:<30} {:<15} {:<15} {:<15} {:<10}".format("ClassID", "roomID", "Start time", "End time", "Capacity"))
        for cls in non_ran_classes:
            print("{:<30} {:<15} {:<15} {:<15} {:<10}".format(cls[0],
                                                              cls[1],
                                                              str(cls[2].strftime("%Y/%m/%d/%H")),
                                                              str(cls[3].strftime("%Y/%m/%d/%H")),
                                                              cls[4]))

        # Step 2: select a class
        class_id = None
        class_ids = [cls[0] for cls in non_ran_classes]
        while class_id not in class_ids:
            class_id_str = input(" select class id to teach (B to cancel) > ")
            if class_id_str == "B":
                return
            class_id = int(class_id_str) if class_id_str.isnumeric() else class_id_str

        # Step 3: Create runs relation
        self.db.insert_into('runs', [str(self.trainer_id), str(class_id)], ['trainerid', 'classid'])
        print("\n Trainer now teaches class ID: ", class_id)
        time.sleep(2)

    def see_ran_classes(self):
        # Get ran classes
        runs = self.db.select(['classid'], 'runs', {"WHERE":
                                                        {"operation": "=", "rowA": str(self.trainer_id),
                                                         "rowB": "trainerid"}})
        ran_classes_ids = [run[0] for run in runs]  # unpack tuple as str
        classes = self.db.select(["*"], 'gymclass', {})
        ran_classes = [cls for cls in classes if cls[0] in ran_classes_ids]

        print("\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n")
        print("\n\t\tASSIGNED CLASSES\n")
        print("{:<30} {:<15} {:<15} {:<15} {:<10}".format("ClassID", "roomID", "Start time", "End time", "Capacity"))
        for cls in ran_classes:
            print("{:<30} {:<15} {:<15} {:<15} {:<10}".format(cls[0],
                                                              cls[1],
                                                              str(cls[2].strftime("%Y/%m/%d/%H")),
                                                              str(cls[3].strftime("%Y/%m/%d/%H")),
                                                              cls[4]))

        input("\nPress enter to continue > ")



    def drop_ran_class(self):
        # Step 1: Get ran classes
        runs = self.db.select(['classid'], 'runs', {"WHERE":
                                                        {"operation": "=", "rowA": str(self.trainer_id),
                                                         "rowB": "trainerid"}})
        ran_classes_ids = [run[0] for run in runs]  # unpack tuple as str

        print("\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n")
        # Step 2: select a class to drop
        class_id = None
        while class_id not in ran_classes_ids:
            class_id = int(input("Select class id to stop teaching > "))

        self.db.delete_from('runs', {"operation": "=", "rowA": "classid", "rowB": str(class_id)})
        print("\n Trainer canceled teaching class ID: ", class_id)
        time.sleep(2)