from helpers import *
from db_api.database import Database
from datetime import datetime, timedelta
import time


class Member:
    def __init__(self, member_id: int, db: Database):
        self.member_id = member_id
        self.db = db

    @staticmethod
    def get_member_info(db: Database, member_id: int):
        sel_res = db.select(["*"], "memberinfo", select_options={
            "WHERE": {"operation": "=", "rowA": "memberinfo", "rowB": str(member_id)}
        })
        return sel_res

    @staticmethod
    def register(db: Database):
        print("\n" * 40)
        print("\tMember Registration")

        print("\n - Personal info -")
        first_name = input("First Name: ")
        last_name = input("Last Name: ")
        email = input("Email: ")
        phone_number = input("Phone Number: ")
        dob = get_date_input("Date of birth (YYYY/MM/DD): ")

        print("\n - Emergency Contact Info -")
        ec_first_name = input("Emergency Contact First Name: ")
        ec_last_name = input("Emergency Contact Last Name: ")
        ec_email = input("Emergency Contact Email: ")
        ec_phone_number = input("Emergency Contact Phone Number: ")

        print("\n - Billing Info -")
        address = input("Billing Address: ")
        cc_number = input("Credit Card Number: ")
        cc_expiration = get_date_input("Credit Card Expiration Date (YYYY/MM): ", "%Y/%m")
        cc_sec_code = input("Credit Card SecurityCode: ")

        print("\n - Goals -")
        weight = input("Weight: ")
        target_date = get_date_input("Target Date (YYYY/MM/DD): ")

        mem_end_date = datetime.today() + timedelta(days=30)
        db.insert_into("billinginfo", [address, mem_end_date, cc_number, cc_expiration, cc_sec_code],
                       ["billingaddress", "memenddate", "creditcardnumber", "creditcardexpirydate",
                        "creditcardsecuritycode"])
        billing_info_id = get_last_id(db, "billinginfo", "billinginfoid")

        db.insert_into("contactinfo", [ec_first_name, ec_last_name, ec_email, ec_phone_number],
                       ["firstname", "lastname", "email", "phonenumber"])
        ec_id = get_last_id(db, "contactinfo", "contactid")

        db.insert_into("contactinfo", [first_name, last_name, email, phone_number],
                       ["firstname", "lastname", "email", "phonenumber"])
        contact_id = get_last_id(db, "contactinfo", "contactid")

        db.insert_into("personalinfo", [dob, contact_id, ec_id],
                       ["dateofbirth", "contactid", "emergencycontactid"])
        personal_info_id = get_last_id(db, "personalinfo", "personalinfoid")

        db.insert_into("memberinfo", [personal_info_id, billing_info_id],
                       ["personalinfoid", "billinginfoid"])

        # db.insert_into("fitnessgoal", [False, target_date, weight], ["isachieved", "targetdate", "targetweight"])
        # goal_id = get_last_id(db, "fitnessgoal", "goalid")

        print("\n\nRegistration Successful")
        time.sleep(2)

    def update_member_info(self):
        personal_info_id, billing_info_id, goal_id = \
            self.db.select(['personalinfoid', 'billinginfoid', 'goalid'], 'memberinfo', select_options={
                "WHERE": {"operation": "=", "rowA": "memberinfo", "rowB": str(self.member_id)}
            })[0]

        contact_id, e_contact_id = \
            self.db.select(['contactid', 'emergencycontactid'], 'personalinfo', select_options={
                "WHERE": {"operation": "=", "rowA": "personalinfoid", "rowB": str(personal_info_id)}
            })[0]

        while True:
            print("\n" * 40)
            options = ["Email", "Phone Number", "Emergency Contact Information", "Billing Information", "Back"]
            option = get_option_input(options, "Select the information to update", 2)

            if option == 0:
                contact_id, email = \
                    self.db.select(['contactid', 'email'], 'contactinfo',
                                   select_options={
                                       "WHERE": {"operation": "=", "rowA": "contactid", "rowB": str(contact_id)}
                                   })[0]

                print("\nYour current email: " + email)
                new_email = input("Enter Your New Email: ")

                upd_res = self.db.update("contactinfo", [("email", new_email)],
                                         {"operation": "=", "rowA": "contactid", "rowB": str(contact_id)})

                print("\nYour email is updated successfully")
                time.sleep(2)

            elif option == 1:
                contact_id, phone_number = \
                    self.db.select(['contactid', 'phonenumber'], 'contactinfo',
                                   select_options={
                                       "WHERE": {"operation": "=", "rowA": "contactid", "rowB": str(contact_id)}
                                   })[0]

                print("\nYour current phone number: " + phone_number)
                new_phone = input("Enter Your New Phone Number: ")

                upd_res = self.db.update("contactinfo", [("phonenumber", new_phone)],
                                         {"operation": "=", "rowA": "contactid", "rowB": str(contact_id)})

                print("\nYour phone number is updated successfully")
                time.sleep(2)

            elif option == 2:
                print("\n - Updating Emergency Contact Info -")
                ec_first_name = input("Emergency Contact First Name: ")
                ec_last_name = input("Emergency Contact Last Name: ")
                ec_email = input("Emergency Contact Email: ")
                ec_phone_number = input("Emergency Contact Phone Number: ")

                upd_res = self.db.update("contactinfo", [("firstname", ec_first_name), ("lastname", ec_last_name),
                                                         ("email", ec_email), ("phonenumber", ec_phone_number)],
                                         {"operation": "=", "rowA": "contactid", "rowB": str(e_contact_id)})

                print("\nYour emergency contact information is updated successfully")
                time.sleep(2)

            elif option == 3:
                print("\n - Updating Billing Information -")
                address = input("Billing Address: ")
                cc_number = input("Credit Card Number: ")
                cc_expiration = get_date_input("Credit Card Expiration Date (YYYY/MM): ", "%Y/%m")
                cc_sec_code = input("Credit Card SecurityCode: ")

                upd_res = self.db.update("billinginfo", [("billingaddress", address), ("creditcardnumber", cc_number),
                                                         ("creditcardexpirydate", cc_expiration),
                                                         ("creditcardsecuritycode", cc_sec_code)],
                                         {"operation": "=", "rowA": "billinginfoid", "rowB": str(billing_info_id)})

                print("\nYour billing information is updated successfully")
                time.sleep(2)

            elif option == 4:
                return

    def display_dashboard(self):
        print("\n Dashboard")

    def register_for_class(self):
        print("\n" * 40)
        print("\t\tCLASS REGISTRATION")

        classes = self.db.select(['classid', 'roomid', 'startdate', 'enddate', 'capacity'], 'gymclass', select_options={
            "WHERE": {"operation": ">", "rowA": "startdate", "rowB": datetime.today().strftime("%Y/%m/%d")}
        })
        classes = [c for c in classes if not self._is_class_available_for_registration(c, self.member_id)]

        if len(classes) == 0:
            print("\nNo classes are available for registration at this time!")
            time.sleep(2)
            return

        print("\n\t\tAVAILABLE CLASSES\n")
        print("{:<10} {:<10} {:<15} {:<15} {:<10}".format("ClassID", "roomID", "Start time", "End time", "Capacity"))
        for cls in classes:
            print("{:<10} {:<10} {:<15} {:<15} {:<10}".format(cls[0],
                                                              cls[1],
                                                              str(cls[2].strftime("%Y/%m/%d/%H")),
                                                              str(cls[3].strftime("%Y/%m/%d/%H")),
                                                              cls[4]))
        classIDs = [c[0] for c in classes]
        classId = get_int_input("\nEnter the class ID register: ")
        while not classId in classIDs:
            print("Invalid class id!")
            classId = get_int_input("Enter a valid class ID register: ")

        self.db.insert_into("participates", [classId, self.member_id], ["classid", "memberid"])

        print("\nSuccessfully registered for class")
        time.sleep(2)

    def _is_class_available_for_registration(self, cls, memberid):
        class_id, room_id, start_date, end_date, capacity = cls
        participants = self.db.select(['memberid'], 'participates', select_options={
            "WHERE": {"operation": "=", "rowA": "classid", "rowB": str(class_id)}
        })
        return len(participants) < int(capacity) and any(p[0] == memberid for p in participants)

    def show_main_menu(self):
        while True:
            print("\n" * 50)
            main_menu_options = ["Update User Info", "Display Dashboard", "Register For Class", "Back"]
            selected_option = get_option_input(main_menu_options, "Member Menu", 2)

            if selected_option == 0:
                self.update_member_info()
            elif selected_option == 1:
                self.display_dashboard()
            elif selected_option == 2:
                self.register_for_class()
            elif selected_option == 3:
                return
