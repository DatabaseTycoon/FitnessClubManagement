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
            main_menu_options = ["View Member Profile", "Sets Available Times", "Back"]
            selected_option = get_option_input(main_menu_options, "Trainer Menu", 2)

            if selected_option == 0:
                print("Selected: View Member Profile")
                self.view_profile()
            elif selected_option == 1:
                print("Selected: Sets Available Times")
            elif selected_option == 2:
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
