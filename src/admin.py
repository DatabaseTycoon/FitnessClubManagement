from helpers import *
from db_api.database import Database
import time


class Admin:
    def __init__(self, admin_id: int, staff_id: int, db: Database):
        self.admin_id = admin_id
        self.staff_id = staff_id
        self.db = db

    def show_main_menu(self):
        while True:
            print("\n" * 50)
            main_menu_options = ["Manage Booked Rooms", "Update Class Schedule", "Equipment Maintenance Monitoring",
                                "Billment And Payment", "Back"]
            selected_option = get_option_input(main_menu_options, "Admin Menu", 2)
            if selected_option == 0:
                print("Selected: Book class (manage booked rooms)")
                capacity = get_int_input(" > Please enter a capacity for the class ", 0, 20)
                start_time = get_datetime_input(" > Please enter a start time for the class")
                end_time = get_datetime_input(" > Please enter an end time for the class")
                equipment_name_in = input("> Please enter a comma seperated list of required equipment for the class "
                                        "(leave empty if N/A): ")
                equipment_names = [name.strip() for name in equipment_name_in.split(",")]
                self.book_class(capacity, start_time, end_time, equipment_names)
            elif selected_option == 1:
                print("Selected: Update Class Schedule")
            elif selected_option == 2:
                self.equipment_maintenance_monitoring()
            elif selected_option == 3:
                self.billment_and_payment()
            elif selected_option == 4:
                return


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

            option_list = ["Sort by room", "Sort by status", "Filter for Working", "Filter for Maintenance",
                           "Filter for Out of Order", "Back"]
            option = get_option_input(option_list)

            if option == 0:
                filtered_equipment_data = equipment_data
                filtered_equipment_data.sort(key=lambda e: e[1])
            elif option == 1:
                filtered_equipment_data = equipment_data
                filtered_equipment_data.sort(key=lambda e: e[2])
            elif option == 2:
                filtered_equipment_data = list(filter(lambda e: e[2] == 'Working', equipment_data))
            elif option == 3:
                filtered_equipment_data = list(filter(lambda e: e[2] == 'Maintenance', equipment_data))
            elif option == 4:
                filtered_equipment_data = list(filter(lambda e: e[2] == 'Out of Order', equipment_data))
            elif option == 5:
                return


    def billment_and_payment(self):
        members = self.db.select(['memberinfo', 'personalinfoid', 'billinginfoid'], 'memberinfo', {})
        p_info = self.db.select(['personalinfoid', 'contactid'], 'personalinfo', {})
        c_info = self.db.select(['contactid', 'firstname', 'lastname', 'email'], 'contactinfo', {})
        b_info = self.db.select(['*'], 'billinginfo', {})

        while True:
            print("\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n")
            print("\n\t\tBILLING MENU\n")
            print("\n\t\tMEMBERS LIST\n")

            print("{:<10} {:<20} {:<20} {:<10}".format("MemberID", "First Name", "Last Name", "Email"))
            for member in members:
                member_pinfo = list(filter(lambda personal: personal[0] == member[1], p_info))[0]
                member_contact = list(filter(lambda contact: contact[0] == member_pinfo[1], c_info))[0]
                print("{:<10} {:<20} {:<20} {:<10}".format(member[0], member_contact[1], member_contact[2], member_contact[3]))

            error = False
            print("\n- B to go Back -")
            ans = input("\nMemberID > ")
            if ans == 'B':
                return
            
            if not ans.isnumeric():
                error = True
            else:    
                chosen_member = list(filter(lambda m: m[0] == int(ans), members))
                if not chosen_member:
                    error = True
                else:
                    chosen_member = chosen_member[0]
                    member_binfo = list(filter(lambda billing: billing[0] == chosen_member[2], b_info))[0]
                    self._show_billing(member_binfo)

            if error:
                print("\nInvalid.\n")
                time.sleep(2)
                
    
    def _show_billing(self, billing_info):
        print("\n" * 50)
        billing_info = billing_info[1:]

        adr = billing_info[0]
        join = str(billing_info[1])
        cnum_string = str(billing_info[2])
        censor_card_num = "***.." + cnum_string[len(cnum_string) - 3:]
        censor_exp_date = "****-**-**"
        censor_cvv = "***"

        print("\n\t\tBILLING INFO --- BILL THIS MEMBER ?\n")
        print("{:<30} {:<15} {:<15} {:<15} {:<10}".format("Address", "Join Date", "Card Num", "Exp", "CVV"))
        print("{:<30} {:<15} {:<15} {:<15} {:<10}".format(adr, join, censor_card_num, censor_exp_date, censor_cvv))

        options = ["YES", "NO"]
        option = get_option_input(options)
        if option == 0:
            print("\n\nMEMBER HAS BEEN BILLED\n")
            print("RETURN TO MEMBER SELECT...\n\n")
            time.sleep(2)
        elif option == 1:
            print("\n\nRETURN TO MEMBER SELECT...\n\n")
            time.sleep(2)



    def book_class(self, class_capacity: int, start_time, end_time, equipment_names: list[str] = None):
        available_rooms = self._get_available_rooms(start_time, end_time, equipment_names)

        if not available_rooms:
            print('\n--No rooms available for booking--\n')
            time.sleep(2)
            return

        # Create a new class
        self.db.insert_into('gymclass',
                            [available_rooms.pop()[0], start_time, end_time, class_capacity],
                            ['roomid', 'startdate', 'enddate', 'capacity'])

        print('\n--Booked class--\n')
        time.sleep(2)

    def _get_bookings(self, time_start, time_end) -> set[tuple[str]]:
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
        all_classes = get_all(self.db, 'gymclass')
        bookings = []
        for cls in all_classes:
            # If either start/end times fall within a booked class time, add to bookings list
            if not (is_before(time_start, time_end, cls[START_INDEX]) or is_after(time_start, time_end, cls[END_INDEX])):
                bookings.append((cls[ROOM_INDEX],))
        return set(bookings)


    def _get_equipment_rooms(self, equipment_names) -> set[tuple[str]]:
        NAME_INDEX = 3
        ROOM_INDEX = 1
        all_equipment = get_all(self.db, 'equipment')
        equipment_rooms = set()
        for equipment in all_equipment:
            # If there exists a name in the given list which matches the current equipment name,
            #   save the room the equipment is in. Note: Capacity/Counts are considered out of scope atm
            if (name for name in equipment_names if name == equipment[NAME_INDEX]):
                equipment_rooms.add((equipment[ROOM_INDEX],))
        return equipment_rooms


    def _get_available_rooms(self,
                             time_start: datetime,
                             time_end: datetime,
                             equipment_names: list[str] = None) -> set[tuple[str]]:
        """
        Return view of booked rooms at a particular time.

        :param time_start:
        :param time_end:
        :param db:
        :return: Room IDs of rooms available for bookings, which have the equipment specified (if applicable)
        """
        # Filter out booked rooms from all rooms
        all_rooms = set(get_all(self.db, 'room'))  # Returns IDs, should be unique
        # Find which classes correspond to bookings at given times
        all_bookings = self._get_bookings(time_start, time_end)
        # Find rooms with matching equipment needs (no needs, all rooms accepted)
        all_equipment_rooms = all_rooms if not equipment_names else self._get_equipment_rooms(equipment_names)

        # Return query result by applying filters (with intersection + subtraction)
        return all_equipment_rooms.intersection(all_rooms - all_bookings)
