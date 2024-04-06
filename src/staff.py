from db_api.database import Database


class Staff:
    @staticmethod
    def get_staff_info(db: Database, staff_id: int):
        sel_res = db.select(["*"], "isadmin", select_options={
            "WHERE": {"operation": "=", "rowA": "staffid", "rowB": str(staff_id)}
        })
        if len(sel_res) > 0:
            return ["Admin", sel_res[0][0]]

        sel_res = db.select(["*"], "istrainer", select_options={
            "WHERE": {"operation": "=", "rowA": "staffid", "rowB": str(staff_id)}
        })
        if len(sel_res) > 0:
            return ["Trainer", sel_res[0][0]]
        return None
