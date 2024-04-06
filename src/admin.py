from helpers import *
from db_api.database import Database


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
            print("Selected: Billment And Payment")

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
