from helpers import *
from db_api.database import Database


class Trainer:
    def __init__(self, trainer_id: int, staff_id: int, db: Database):
        self.trainer_id = trainer_id
        self.staff_id = staff_id
        self.db = db

    def show_main_menu(self):
        print("\n" * 50)
        main_menu_options = ["View Member Profile", "Sets Available Times"]
        selected_option = get_option_input(main_menu_options, "Trainer Menu", 2)

        if selected_option == 0:
            print("Selected: View Member Profile")
        elif selected_option == 1:
            print("Selected: Sets Available Times")
