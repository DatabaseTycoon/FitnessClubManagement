import psycopg
import psycopg.sql as sql

class _WhereHelper():
    def __init__(self, exists: bool, operator: str="", rA: str="", rB: str="") -> None:
        self.has_where = exists
        if not operator in [">", "<", ">=", "<=", "=", ""]:
            raise ValueError("Where operator is not valid: " + operator)
        self.op = operator
        if rA != "":
            self.is_row_A_Literal = rA.isnumeric()
        if rB != "":
            self.is_row_B_Literal = rB.isnumeric()


class _OrderByHelper():
    def __init__(self, exists: bool, ASC: bool=None, rA: str="") -> None:
        self.has_order_by = exists
        self.asc = "ASC" if ASC else "DESC"

class Database():

    def __init__(self, db_name: str, user_name: str, password: str, port: str) -> None:
        try:
            self.__connection = psycopg.connect(
                f"dbname={db_name} user={user_name} password={password} port={port}"
            )

        except psycopg.OperationalError as e:
            print(e)
            exit(1)


    def __form_sel_querry(self,
                          main: bool,
                          select_all: bool=False,
                          has_limit: bool=False, 
                          has_offset: bool=False, 
                          where_helper: _WhereHelper=_WhereHelper(False), 
                          order_helper: _OrderByHelper=_OrderByHelper(False), 
                          has_union: bool=False, union_op: dict={}) -> sql.SQL:
        
        suff = "main_" if main else "side_"
        ## Where
        if where_helper.has_where:
            where = sql.SQL(f" WHERE {{{suff}where_rowA}} {where_helper.op} {{{suff}where_rowB}} ")
        else:
            where = sql.SQL("")
        
        ## ORDER BY
        if order_helper.has_order_by: #TODO Identifier use here
            order_by = sql.SQL(f" ORDER BY {{{suff}order_by_rowA}} {order_helper.asc}")

            if has_limit: #TODO use sql.Literal
                limit = sql.SQL(f" LIMIT {{{suff}limit_num}} ")
            else:
                limit = ""

            if has_offset: #TODO use sql.Literal
                offset = sql.SQL(f" OFFSET {{{suff}offset_num}} ")
        else:
            order_by = sql.SQL("")
            limit = sql.SQL("")
            offset = sql.SQL("")

        # UNION
        if has_union:
            union_sel = self.__form_sel_querry(
                main=False,
                has_limit=bool(union_op.get("LIMIT", False)),
                has_offset=bool(union_op.get("OFFSET", False)),
                order_helper=_OrderByHelper(bool(union_op.get("LIMIT", False)), union_op.get("LIMIT", False)),
                where_helper=_WhereHelper(bool(union_op.get("WHERE", False)), union_op.get("WHERE")["operation"], union_op.get("WHERE")["rowA"], union_op.get("WHERE")["rowB"])
            )
            union = sql.SQL(f" {{{union_sel}}} ")
        else:
            union = sql.SQL("")
        
        rows = f'{{{suff}rows}}' if not select_all else '*'
        return sql.SQL((sql.SQL(f"SELECT {rows} FROM {{{suff}table}}") + where + union + order_by + limit + offset).as_string(self.__connection))
    

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
        elif len(rows) == 0:
            raise TypeError(f"{rows}: cannot be empty")
        
        select_all_rows = rows[0] == "*"
        
        where = select_options.get("WHERE", {"rowA": "", "rowB": "", "operation": ""})
        union = select_options.get("UNION", tuple())
        limit = select_options.get("LIMIT", "")
        offset = select_options.get("OFFSET", "")
        order_by = select_options.get("ORDER_BY", {"rowA": "", "asc": ""})

        w_helper = _WhereHelper(bool(select_options.get("WHERE", False)), where["operation"], where["rowA"], where["rowB"])
        o_helper = _OrderByHelper(bool(select_options.get("ORDER_BY", False)), order_by["asc"])

        querry = self.__form_sel_querry(
            main            =   True,
            select_all      =   select_all_rows,
            has_limit       =   bool(select_options.get("LIMIT", False)),
            has_offset      =   bool(select_options.get("OFFSET", False)),
            order_helper    =   o_helper,
            where_helper    =   w_helper,
            has_union       =   bool(select_options.get("UNION", False)),
            union_op        =   select_options.get("UNION", dict())
        )

        querry = querry.format(
            main_rows           =   sql.SQL(",").join([sql.Identifier(r) for r in rows]),
            main_table          =   sql.Identifier(tbl),
            main_where_rowA     =   sql.Literal(where["rowA"]) if w_helper.is_row_A_Literal else sql.Identifier(where["rowA"]),
            main_where_rowB     =   sql.Literal(where["rowB"]) if w_helper.is_row_B_Literal else sql.Identifier(where["rowB"]),
            main_order_by_rowA  =   sql.Identifier(order_by["rowA"]),
            main_limit_num      =   sql.Literal(limit),
            main_offset_num     =   sql.Literal(offset)
        )


        if union:
            union_rows = ",".join(union[0]) if len(union[0]) > 1 else union[0][0]
            union_table = union[1]
            union_op = union[2]

            u_where = union_op.get("WHERE", {"rowA": "", "rowB": "", "operation": ""})
            u_limit = union_op.get("LIMIT", "")
            u_offset = union_op.get("OFFSET", "")
            u_order_by = union_op.get("ORDER_BY", {"rowA": "", "asc": ""})

            querry = querry.format(
                side_rows           =   sql.SQL(",").join([sql.Identifier(r) for r in union_rows]),
                side_table          =   sql.Identifier(union_table),
                side_where_rowA     =   sql.Identifier(u_where["rowA"]),
                side_where_rowB     =   sql.Identifier(u_where["rowB"]),
                side_order_by_rowA  =   sql.Identifier(u_order_by["rowA"]),
                side_limit_num      =   sql.Literal(u_limit),
                side_offset_num     =   sql.Literal(u_offset)
            )


            with self.__connection.cursor() as cursor:
                cursor.execute()
                self.__connection.commit()
                return cursor.fetchall()
            
        else:
            with self.__connection.cursor() as cursor:
                    cursor.execute(querry)
                    self.__connection.commit()
                    return cursor.fetchall()
