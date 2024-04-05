class Admin:
    def __init__(self, admin_id: int, staff_id: int):
        self.admin_id = admin_id
        self.staff_id = staff_id

    def show_main_menu(self):
        input("Admin Menu " + str(self.admin_id))
