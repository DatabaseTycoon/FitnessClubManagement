import psycopg.errors

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

        print("\n\nRegistration Successful")
        time.sleep(2)

    def update_member_info(self):
        personal_info_id, billing_info_id = \
            self.db.select(['personalinfoid', 'billinginfoid'], 'memberinfo', select_options={
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
        print("\n" * 40)
        print("\t\t\tMEMBER DASHBOARD\n")

        self._show_personal_information()
        self._show_upcoming_classes()
        self._show_statistics()
        self._show_fitness_goals()

        input("\n\n\nPress any key to go back to the main menu...")

    def _show_personal_information(self):
        personal_info_id = self.db.select(['personalinfoid'], 'memberinfo', select_options={
            "WHERE": {"operation": "=", "rowA": "memberinfo", "rowB": str(self.member_id)}
        })[0][0]

        contact_id, dob = self.db.select(['contactid', 'dateofbirth'], 'personalinfo', select_options={
            "WHERE": {"operation": "=", "rowA": "personalinfoid", "rowB": str(personal_info_id)}
        })[0]

        first_name, last_name, email, phone_number = \
            self.db.select(['firstname', 'lastname', 'email', 'phonenumber'], 'contactinfo', select_options={
                "WHERE": {"operation": "=", "rowA": "contactid", "rowB": str(contact_id)}
            })[0]

        print("\n\tPERSONAL INFORMATION\n")

        print("{:<20} {:<30}".format("First Name: ", first_name))
        print("{:<20} {:<30}".format("Last Name: ", last_name))
        print("{:<20} {:<30}".format("Email: ", email))
        print("{:<20} {:<30}".format("Phone Number: ", phone_number))
        print("{:<20} {:<30}".format("Date of Birth: ", dob.strftime("%d %b, %Y")))

    def _show_statistics(self):
        print("\n" * 2)
        print("\tSTATISTICS\n")
        stats = self.db.select(['type', 'value'], 'statistic', select_options={
            "WHERE": {"operation": "=", "rowA": "memberid", "rowB": str(self.member_id)}
        })

        if len(stats) > 0:
            print(
                "{:<15} {:<30}".format("Type", "Value"))
            for s in stats:
                print("{:<15} {:<30}".format(s[0], s[1]))
        else:
            print("   You don't have any statistics")

    def _show_fitness_goals(self):
        print("\n" * 2)
        print("\tFITNESS GOALS\n")
        goals = self.db.select(['type', 'description', 'isachieved', 'targetdate'], 'fitnessgoal', select_options={
            "WHERE": {"operation": "=", "rowA": "memberid", "rowB": str(self.member_id)}
        })

        current_goals = []
        completed_goals = []
        for goal in goals:
            if goal[2]:
                completed_goals.append(goal)
            else:
                current_goals.append(goal)

        print("Targeted Fitness Goals:\n")
        if len(current_goals) > 0:
            print(
                "{:<15} {:<30} {:<15}".format("Goal Type", "Description", "Target Date"))
            for goal in current_goals:
                print("{:<15} {:<30} {:<15}".format(goal[0], goal[1], str(goal[3].strftime("%Y/%m/%d"))))
        else:
            print("   You don't have any fitness goals")

        print("\nAchievements:\n")
        if len(completed_goals) > 0:
            print(
                "{:<15} {:<30} {:<15}".format("Goal Type", "Description", "Achievement Date"))
            for goal in completed_goals:
                print("{:<15} {:<30} {:<15}".format(goal[0], goal[1], str(goal[3].strftime("%Y/%m/%d"))))
        else:
            print("   You don't have any achieved fitness goals")

    def _show_upcoming_classes(self):
        print("\n" * 2)
        print("\n\tUPCOMING CLASSES\n")
        classIDs = self.db.select(['classid'], 'participates', select_options={
            "WHERE": {"operation": "=", "rowA": "memberid", "rowB": str(self.member_id)}
        })
        classIDs = [c[0] for c in classIDs]
        if len(classIDs) == 0:
            print("You don't have any upcoming classes")
        else:
            where_conditions = []
            for classID in classIDs:
                where_conditions.append({"operation": "=", "rowA": "classid", "rowB": str(classID)})
            classes = self.db.select_with_or(["*"], "gymclass", *where_conditions)

            upcomingClasses = list(filter(lambda c: (c[2] > datetime.now()), classes))

            print(
                "{:<10} {:<10} {:<15} {:<15} {:<10}".format("ClassID", "roomID", "Start time", "End time", "Capacity"))
            for cls in upcomingClasses:
                print("{:<10} {:<10} {:<15} {:<15} {:<10}".format(cls[0],
                                                                  cls[1],
                                                                  str(cls[2].strftime("%Y/%m/%d/%H")),
                                                                  str(cls[3].strftime("%Y/%m/%d/%H")),
                                                                  cls[4]))

    def register_for_class(self):
        print("\n" * 40)
        print("\t\tCLASS REGISTRATION")

        classes = self.db.select(['classid', 'roomid', 'startdate', 'enddate', 'capacity'], 'gymclass', select_options={
            "WHERE": {"operation": ">", "rowA": "startdate", "rowB": datetime.today().strftime("%Y/%m/%d")}
        })
        classes = [c for c in classes if self._is_class_available_for_registration(c, self.member_id)]

        if len(classes) == 0:
            print("\n\tNo classes are available for registration at this time!")
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

    def add_statistics(self):
        while True:
            print("\n" * 40)
            print("\tADD NEW STATISTICS\n")

            print("Enter new statistics details:")
            type = input("Type: ")

            stats = self.db.select(['type', 'value'], 'statistic', select_options={
                "WHERE": {"operation": "=", "rowA": "memberid", "rowB": str(self.member_id)}
            })
            types = [s[0] for s in stats]

            if type in types:
                print("\nYou already have a statistics with the same type.")
                option = get_option_input(["Add a different statistics", "Back"])
                if option == 0:
                    continue
                else:
                    break

            value = input("Value: ")

            self.db.insert_into("statistic", [self.member_id, type, value], ["memberid", "type", "value"])

            print("\nStatistics successfully added!")
            time.sleep(2)
            break

    def manage_fitness_goals(self):
        print("\n" * 40)
        print("\tMANAGE FITNESS GOALS\n")

        option = get_option_input(["Add a new goal goal", "Set Goal As Achieved", "Back"])
        if option == 0:
            self._add_fitness_goal()
        elif option == 1:
            self._set_goal_as_achieved()
        elif option == 2:
            return

    def _set_goal_as_achieved(self):
        print("\n" * 40)
        goals = self.db.select(['type', 'description', 'isachieved', 'targetdate'], 'fitnessgoal', select_options={
            "WHERE": {"operation": "=", "rowA": "memberid", "rowB": str(self.member_id)}
        })

        current_goals = []
        types = []
        for goal in goals:
            if not goal[2]:
                current_goals.append(goal)
                types.append(goal[0])

        print("Fitness Goals:\n")
        if len(current_goals) > 0:
            print("{:<15} {:<30} {:<15}".format("Type", "Description", "Target Date"))
            for goal in current_goals:
                print("{:<15} {:<30} {:<15}".format(goal[0], goal[1], str(goal[3].strftime("%Y/%m/%d"))))

            type_to_update = input("\nEnter the type of the fitness goal you achieved: ")
            while not type_to_update in types:
                print("Invalid type!")
                type_to_update = input("Enter the type of the fitness goal you achieved: ")

            upd_res = self.db.update("fitnessgoal", [("isachieved", str(1))],
                                     {"operation": "=", "rowA": "memberid", "rowB": str(self.member_id)},
                                     {"operation": "=", "rowA": "type", "rowB": str(type_to_update)})

            stats = self.db.select(['type', 'value'], 'statistic', select_options={
                "WHERE": {"operation": "=", "rowA": "memberid", "rowB": str(self.member_id)}
            })
            stats_types = [s[0] for s in stats]

            # Updating the statistic table with the new archived goal
            if type_to_update in stats_types:
                goal = list(filter(lambda g: g[0] == type_to_update, current_goals))[0]

                upd_res = self.db.update("statistic", [("value", goal[1])],
                                         {"operation": "=", "rowA": "memberid", "rowB": str(self.member_id)},
                                         {"operation": "=", "rowA": "type", "rowB": str(type_to_update)})
            else:
                self.db.insert_into("statistic", [self.member_id, type_to_update, goal[1]], ["memberid", "type", "value"])

            print("Congratulations! Updated your goal as Achieved.")
            time.sleep(2)

        else:
            print("   You don't have any fitness goals to achieve")
            time.sleep(2)


    def _add_fitness_goal(self):
        while True:
            print("\n" * 40)
            print("\tAdd New Fitness Goal\n")

            print("Enter new goal details:")
            type = input("Type: ")

            types = self.db.select(['type'], 'fitnessgoal', select_options={
                "WHERE": {"operation": "=", "rowA": "memberid", "rowB": str(self.member_id)}
            })
            types = [t[0] for t in types]

            if type in types:
                print("\nYou already have a goal with the same type.")
                option = get_option_input(["Add a different goal", "Back"])
                if option == 0:
                    continue
                else:
                    break

            description = input("Description: ")
            target_date = get_date_input("Target Date (YYYY/MM/DD): ")

            self.db.insert_into("fitnessgoal", [self.member_id, type, description, False, target_date],
                                ["memberid", "type", "description", "isachieved", "targetdate"])

            print("\nGoal successfully added!")
            time.sleep(2)
            break

    def _is_class_available_for_registration(self, cls, memberid):
        class_id, room_id, start_date, end_date, capacity = cls
        participants = self.db.select(['memberid'], 'participates', select_options={
            "WHERE": {"operation": "=", "rowA": "classid", "rowB": str(class_id)}
        })
        return len(participants) < int(capacity) and not any(p[0] == memberid for p in participants)

    def show_main_menu(self):
        while True:
            print("\n" * 50)
            main_menu_options = ["Update User Info", "Display Dashboard", "Register For Class", "Add Statistics",
                                 "Manage Fitness Goals", "Back"]
            selected_option = get_option_input(main_menu_options, "Member Menu", 2)

            if selected_option == 0:
                self.update_member_info()
            elif selected_option == 1:
                self.display_dashboard()
            elif selected_option == 2:
                self.register_for_class()
            elif selected_option == 3:
                self.add_statistics()
            elif selected_option == 4:
                self.manage_fitness_goals()
            elif selected_option == 5:
                return
