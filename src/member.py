from helpers import *
from db_api.database import Database
import time


class Member:
    def __init__(self, member_id: int, db: Database):
        self.memberId = member_id
        self.db = db

    def show_main_menu(self):
        input("Member Menu " + str(self.memberId))

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
        cc_expiration = input("Credit Card Expiration Date: ")
        cc_sec_code = input("Credit Card SecurityCode: ")

        print("\n - Goals -")
        weight = input("Weight: ")
        targetDate = get_date_input("Target Date (YYYY/MM/DD): ")

        # TODO: Insert the user data to relevant tables
        # db.insert_into("fitnessgoal", [2, False, targetDate, weight], ["goalid", "isachieved", "targetdate", "targetweight"])

        # MemberInfo(memberInfo, personalInfoID, billingInfoID, statID, goalID)
        # FitnessGoal(goalID, isAchieved, targetDate, targetWeight)
        # BillingInfo(billingInfoID, billingAddress, memEndDate, creditCardNumber, creditCardExpiryDate, creditCardSecurityCode)
        # PersonalInfo(personalInfoID, nameID, emergencyContactID, dateOfBirth, email, phoneNumber)
        # EmergencyContact(emergencyContactID, nameID, dateOfBirth, email, phoneNumber)

    def show_main_menu(self):
        print("\n" * 50)
        main_menu_options = ["Update User Info", "Display Dashboard", "Register For Class"]
        selected_option = get_option_input(main_menu_options, "Member Menu", 2)

        if selected_option == 0:
            print("Selected: Update User Info")
        elif selected_option == 1:
            print("Selected: Display Dashboard")
        elif selected_option == 2:
            print("Selected: Register For Class")
        
        time.sleep(2)
