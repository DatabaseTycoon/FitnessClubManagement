import psycopg

class Database():

    def __init__(self, db_name: str, user_name: str, password: str, port: str) -> None:
        try:
            self.__connection = psycopg.connect(
                f"dbname={db_name} user={user_name} password={password} port={port}"
            )

        except psycopg.OperationalError as e:
            print(e)
            exit(1)


    def __form_sel_querry(main: bool,
                          has_limit: bool=False, 
                          has_offset: bool=False, 
                          has_where: bool=False, 
                          has_order_by: bool=False, 
                          has_union: bool=False, union_op: dict={}):
        
        suff = "main_" if main else "side_"
        ## Where
        if has_where:
            where = f" WHERE %{{{suff}where_rowA}}s %{{{suff}where_op}}s %{{{suff}where_rowB}}s " 
        else:
            where = ""
        
        ## ORDER BY
        if has_order_by:
            order_by = f" ORDER BY %{{{suff}order_by_rowA}}s %{{{suff}order_by_asc}}s "

            if has_limit:
                limit = f" LIMIT %{{{suff}limit_num}}s "
            else:
                limit = ""

            if has_offset:
                offset = f" OFFSET %{{{suff}offset_num}}s "
        else:
            order_by = ""
            limit = ""
            offset = ""

        # UNION
        if has_union:
            union_sel = Database.__form_sel_querry(
                main=False,
                has_limit=bool(union_op.get("LIMIT", False)),
                has_offset=bool(union_op.get("OFFSET", False)),
                has_order_by=bool(union_op.get("LIMIT", False)),
                has_where=bool(union_op.get("WHERE", False))
            )
            union = f" {{{union_sel}}} "
        else:
            union = ""
        

        return f"SELECT %{{{suff}rows}}s FROM %{{{suff}table}}" + where + union + order_by + limit + offset
    

    def select(self, rows: 'list[str]', tbl: str, select_options: dict):
        """Used to run a select querry on the database

        Args:
            rows (list[str]): Rows to be returned
            tbl (str): The targetted table name
            select_options (dict): Options for the select querry. The format of which should be the following
                ```
                example_select_option = {
                                        # Will do rowA operation rowB
                                        "WHERE": {"operation": ">", "rowA": "name", "rowB": "name2"}, 
                                        # This tuple should contain arguments that will be passed to a select method
                                        "UNION": tuple(), 
                                        "ORDER_BY": {"ASC": True, "rowA": "name"},
                                        "LIMIT": "1",
                                        "OFFSET": "1",
                                    }
                ```

        Raises:
            TypeError: If the parameters malformed
        """
        # Validate Params
        if type(rows) != list:
            raise TypeError(f"{rows}: not a list")
        
        where = select_options.get("WHERE", {"rowA": "", "rowB": "", "operation": ""})
        union = select_options.get("UNION", tuple())
        limit = select_options.get("LIMIT", "")
        offset = select_options.get("OFFSET", "")
        order_by = select_options.get("ORDER_BY", {})

        querry_string = Database.__form_sel_querry(
            main=True,
            has_limit=bool(select_options.get("LIMIT", False)),
            has_offset=bool(select_options.get("OFFSET", False)),
            has_order_by=bool(select_options.get("LIMIT", False)),
            has_where=bool(select_options.get("WHERE", False)),
            has_union=bool(select_options.get("UNION", False)),
            union_op=select_options.get("UNION", dict())
        )

        if union:
            union_rows = ",".join(union[0]) if len(union[0]) > 1 else union[0][0]
            union_table = union[1]
            union_op = union[2]

            u_where = union_op.get("WHERE", {"rowA": "", "rowB": "", "operation": ""})
            u_limit = union_op.get("LIMIT", "")
            u_offset = union_op.get("OFFSET", "")
            u_order_by = union_op.get("ORDER_BY", {})


            with self.__connection.cursor() as cursor:
                cursor.execute(querry_string, {
                    "main_rows": ",".join(rows) if len(rows) > 1 else rows[0],
                    "main_table": tbl,
                    "side_rows": union_rows,
                    "side_table": union_table,
                    "main_where_rowA": where["rowA"],
                    "main_where_rowB": where["rowB"],
                    "main_where_op": where["operation"],
                    "side_where_rowA": u_where["rowA"],
                    "side_where_rowB": u_where["rowB"],
                    "side_where_op": u_where["operation"],
                    "main_order_by_rowA": order_by["rowA"],
                    "main_order_by_asc": order_by["asc"],
                    "side_order_by_rowA": u_order_by["rowA"],
                    "side_order_by_asc": u_order_by["asc"],
                    "main_limit_num": limit,
                    "side_limit_num": u_limit,
                    "main_offset_num": offset,
                    "side_offset_num": u_offset
                })
                self.__connection.commit()
                return cursor.fetchall()
            
        else:
            with self.__connection.cursor() as cursor:
                    cursor.execute(querry_string, {
                        "main_rows": ",".join(rows) if len(rows) > 1 else rows[0],
                        "main_table": tbl,
                        "main_where_rowA": where["rowA"],
                        "main_where_rowB": where["rowB"],
                        "main_where_op": where["operation"],
                        "main_order_by_rowA": order_by["rowA"],
                        "main_order_by_asc": order_by["asc"],
                        "main_limit_num": limit,
                        "main_offset_num": offset,
                    })
                    self.__connection.commit()
                    return cursor.fetchall()





