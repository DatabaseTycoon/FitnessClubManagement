from helpers import *
from db_api.database import Database
import time


class Admin:
    def __init__(self, admin_id: int, staff_id: int, db: Database):
        self.admin_id = admin_id
        self.staff_id = staff_id
        self.db = db

    def show_main_menu(self):
        print("\n" * 50)
        main_menu_options = ["Manage Booked Rooms", "Update Class Schedule", "Equipment Maintenance Monitoring",
                             "Billment And Payment"]
        selected_option = get_option_input(main_menu_options, "Admin Menu", 2)

        if selected_option == 0:
            print("Selected: Manage Booked Rooms")
        elif selected_option == 1:
            print("Selected: Update Class Schedule")
        elif selected_option == 2:
            self.equipment_maintenance_monitoring()
        elif selected_option == 3:
            self.billment_and_payment()

    def equipment_maintenance_monitoring(self):
        equipment_data = self.db.select(["*"], "equipment", select_options={})
        filtered_equipment_data = equipment_data

        while True:
            print("\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n")

            # Print equipment information in a tabular format
            print("\n\t\tEQUIPMENT MAINTENANCE MONITORING\n")
            print("{:<10} {:<15} {:<30} {:<10}".format("Equip ID", "Status", "Equipment Name", "Room ID"))
            print("{:<10} {:<15} {:<30} {:<10}".format("--------", "------", "--------------", "-------"))
            for equipment_id, room_id, status, equipment_name in filtered_equipment_data:
                print("{:<10} {:<15} {:<30} {:<10}".format(equipment_id, status, equipment_name, room_id))

            option_list = ["Quit", "Sort by room", "Sort by status", "Filter for Working", "Filter for Maintenance",
                      "Filter for Out of Order"]
            option = get_option_input(option_list)

            if option == 0:
                break
            if option == 1:
                filtered_equipment_data = equipment_data
                filtered_equipment_data.sort(key=lambda e: e[1])
            elif option == 2:
                filtered_equipment_data = equipment_data
                filtered_equipment_data.sort(key=lambda e: e[2])
            elif option == 3:
                filtered_equipment_data = list(filter(lambda e: e[2] == 'Working', equipment_data))
            elif option == 4:
                filtered_equipment_data = list(filter(lambda e: e[2] == 'Maintenance', equipment_data))
            elif option == 5:
                filtered_equipment_data = list(filter(lambda e: e[2] == 'Out of Order', equipment_data))

        self.show_main_menu()
    

    def billment_and_payment(self):
        members = self.db.select(['memberinfo', 'personalinfoid', 'billinginfoid'], 'memberinfo', {})
        p_info = self.db.select(['personalinfoid', 'contactid'], 'personalinfo', {})
        c_info = self.db.select(['contactid', 'firstname', 'lastname', 'email'], 'contactinfo', {})
        b_info = self.db.select(['*'], 'billinginfo', {})

        while True:
            print("\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n")
            print("\n\t\tBILLING MENU\n")
            print("\n\t\tMEMBERS LIST\n")

            print("{:<10} {:<15} {:<30} {:<10}".format("MemberID", "First Name", "Last Name", "Email"))
            for member in members:
                member_pinfo = list(filter(lambda personal: personal[0] == member[1], p_info))[0]
                member_contact = list(filter(lambda contact: contact[0] == member_pinfo[1], c_info))[0]
                print("{:<10} {:<15} {:<30} {:<10}".format(member[0], member_contact[1], member_contact[2], member_contact[3]))

            error = False
            print("- Q to quit -")
            ans = input("\nMemberID > ")
            if ans == 'Q':
                return
            
            if not ans.isnumeric():
                error = True
            else:    
                chosen_member = list(filter(lambda m: m[0] == int(ans), members))[0]
                if not chosen_member:
                    error = True
                else:
                    member_binfo = list(filter(lambda billing: billing[0] == chosen_member[2], b_info))[0]
                    self._show_billing(member_binfo)

            if error:
                print("\nInvalid.\n")
                time.sleep(2)
                

        print("\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n")
    
    def _show_billing(self, billing_info):
        print("\n" * 50)
        billing_info = billing_info[1:]

        print("\n\t\tBILLING INFO\n")
        print("{:<30} {:<15} {:<15} {:<15} {:<10}".format("Address", "Join Date", "Card Num", "Exp", "CVV"))
        print("{:<30} {:<15} {:<15} {:<15} {:<10}".format(billing_info[0], str(billing_info[1]), billing_info[2], str(billing_info[3]), billing_info[4]))

        options = ["YES", "NO"]
        option = get_option_input(options)
        if option == 0:
            print("\n\nMEMBER HAS BEEN BILLED\n")
            print("RETURN TO MEMBER SELECT...\n\n")
            time.sleep(2)
        elif option == 1:
            print("\n\nRETURN TO MEMBER SELECT...\n\n")
            time.sleep(2)





