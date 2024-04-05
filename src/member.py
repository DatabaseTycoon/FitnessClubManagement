from helpers import *
from src.db_api.database import Database


class Member:
    def __init__(self, member_id: int):
        self.memberId = member_id

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
        print("\n"*40)
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

        db.insert_into("fitnessgoal", [2, False, targetDate, weight], ["goalid", "isachieved", "targetdate", "targetweight"])

        # MemberInfo(memberInfo, personalInfoID, billingInfoID, statID, goalID)
        # FitnessGoal(goalID, isAchieved, targetDate, targetWeight)
        # BillingInfo(billingInfoID, billingAddress, memEndDate, creditCardNumber, creditCardExpiryDate, creditCardSecurityCode)
        # PersonalInfo(personalInfoID, nameID, emergencyContactID, dateOfBirth, email, phoneNumber)
        # EmergencyContact(emergencyContactID, nameID, dateOfBirth, email, phoneNumber)

        # insert_into(self, tbl: str, values: 'list[str]', rows: 'list[str]' = None):
        #     """Inserts specified values into specified rows for a specified table in the database
        #
        #     Args:
        #         tbl (str): The target table
        #         values (list[str]): A list of values to insert
        #         rows (list[str], optional): The rows to add. Defaults to None, when defaulted to None assumes all rows.

        # sel_res = db.select(["*"], "memberinfo", select_options={
        #     "WHERE": {"operation": "=", "rowA": "memberinfo", "rowB": str(member_id)}
        # })
        # return sel_res

