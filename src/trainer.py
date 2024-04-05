from helpers import *


class Trainer:
    def __init__(self, trainer_id: int, staff_id: int):
        self.trainer_id = trainer_id
        self.staff_id = staff_id

    def show_main_menu(self):
        input("Trainer Menu " + str(self.trainer_id))
