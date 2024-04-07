from helpers import *
from db_api.database import Database
from datetime import datetime, timedelta
import time


class Member:
    def __init__(self, member_id: int, db: Database):
        self.member_id = member_id
        self.db = db

    def show_main_menu(self):
        input("Member Menu " + str(self.member_id))

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

        db.insert_into("fitnessgoal", [False, target_date, weight], ["isachieved", "targetdate", "targetweight"])
        goal_id = get_last_id(db, "fitnessgoal", "goalid")

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

        db.insert_into("memberinfo", [personal_info_id, billing_info_id, goal_id],
                       ["personalinfoid", "billinginfoid", "goalid"])

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
                print("Selected: Register For Class")
            elif selected_option == 3:
                return
