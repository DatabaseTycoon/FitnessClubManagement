import psycopg
import psycopg.sql as sql

class _WhereHelper():
    def __init__(self, exists: bool, column_names: 'list[str]', operator: str="", rA: str="", rB: str="") -> None:
        self.has_where = exists
        if not operator in [">", "<", ">=", "<=", "=", ""]:
            raise ValueError("Where operator is not valid: " + operator)
        self.op = operator

        self.is_row_A_Literal = (rA.isnumeric() or rA not in column_names) if rA != "" else False
        self.is_row_B_Literal = (rB.isnumeric() or rB not in column_names) if rB != "" else False


class _OrderByHelper():
    def __init__(self, exists: bool, ASC: bool=None) -> None:
        self.has_order_by = exists
        self.asc = "ASC" if ASC else "DESC"


class Database():

    def __init__(self, db_name: str, user_name: str, password: str, port: str) -> None:
        try:
            self.__connection = psycopg.connect(
                f"dbname={db_name} user={user_name} password={password} port={port}"
            )
            self.__row_cache = {}

        except psycopg.OperationalError as e:
            print(e)
            exit(1)


    def __add_cache(self, table: str):
        q = sql.SQL("SELECT * FROM {tbl} LIMIT 0").format(tbl=sql.Identifier(table))
        with self.__connection.cursor() as cursor:
            cursor.execute(q)
            self.__row_cache.update({table : [desc[0] for desc in cursor.description]})


    def __form_del_querry(self, where_helper: _WhereHelper) -> sql.SQL:
        ## Where
        if where_helper.has_where:
            where = sql.SQL(f" WHERE {{where_rowA}} {where_helper.op} {{where_rowB}} ")
        else:
            where = sql.SQL("")
        
        return sql.SQL((sql.SQL(f"DELETE FROM {{table}}") + where).as_string(self.__connection))


    def __form_sel_querry(self,
                          main: bool,
                          table: str,
                          select_all: bool=False,
                          has_limit: bool=False, 
                          has_offset: bool=False, 
                          where_helper: _WhereHelper=_WhereHelper(False, []), 
                          order_helper: _OrderByHelper=_OrderByHelper(False, []), 
                          has_union: bool=False, union_op: dict={}) -> sql.SQL:
        
        pre = "main_" if main else "side_"
        ## Where
        if where_helper.has_where:
            where = sql.SQL(f" WHERE {{{pre}where_rowA}} {where_helper.op} {{{pre}where_rowB}} ")
        else:
            where = sql.SQL("")
        
        ## ORDER BY
        if order_helper.has_order_by: #TODO Identifier use here
            order_by = sql.SQL(f" ORDER BY {{{pre}order_by_rowA}} {order_helper.asc}")

            if has_limit: #TODO use sql.Literal
                limit = sql.SQL(f" LIMIT {{{pre}limit_num}} ")
            else:
                limit = ""

            if has_offset: #TODO use sql.Literal
                offset = sql.SQL(f" OFFSET {{{pre}offset_num}} ")
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
                where_helper=_WhereHelper(bool(union_op.get("WHERE", False)), self.__row_cache[table], union_op.get("WHERE")["operation"], union_op.get("WHERE")["rowA"], union_op.get("WHERE")["rowB"])
            )
            union = sql.SQL(f" {{{union_sel}}} ")
        else:
            union = sql.SQL("")
        
        rows = f'{{{pre}rows}}' if not select_all else '*'
        return sql.SQL((sql.SQL(f"SELECT {rows} FROM {{{pre}table}}") + where + union + order_by + limit + offset).as_string(self.__connection))
    

    def __form_insert_querry(self, has_rows: bool) -> sql.SQL:
        if has_rows:
            rows = sql.SQL(f" ({{rows}})")
        else:
            rows = ''
        return sql.SQL((sql.SQL(f"INSERT INTO {{table}}") + rows + sql.SQL(f" VALUES ({{values}})")).as_string(self.__connection))
    

    def select_with_or(self, rows: 'list[str]', tbl: str, *ORed_conditions: 'dict'):
        """Used to run a select querry with ORed WHERE conditions.

        Args:
            rows (list[str]): Rows to be returned
            tbl (str): The targetted table name
            ORed_conditions (tuple[dict]): A list of dicts formmated as such ``` {"operation": ">", "rowA": "name", "rowB": "name2"} ``` This dict CANNOT be empty.
        """

        if type(rows) != list:
            raise TypeError(f"{rows}: not a list")
        elif len(rows) == 0:
            raise TypeError(f"{rows}: cannot be empty")
        elif [condition for condition in ORed_conditions if not condition]:
            raise TypeError(f"Found empty condition in ORed list: {ORed_conditions}")
        
        select_all_rows = rows[0] == "*"

        # Update Cache
        if tbl not in self.__row_cache:
            self.__add_cache(tbl)

        helped_conditions = [_WhereHelper(True, self.__row_cache[tbl], cond["operation"], cond["rowA"], cond["rowB"]) 
                for cond in ORed_conditions]
        
        string_rows = f'{{rows}}' if not select_all_rows else '*'
        pre_querry = f"SELECT {string_rows} FROM {{table}} WHERE "
        querry = sql.SQL(pre_querry)

        # Not Or
        querry = querry.format(table = sql.Identifier(tbl), rows = sql.SQL(",").join([sql.Identifier(r) for r in rows])).as_string(self.__connection)

        # Or
        for x in range(len(helped_conditions)):
            cond_help = helped_conditions[x]
            cond_obj = ORed_conditions[x]
            OR_statement = "OR " if x != 0 else ""
            querry += f"{OR_statement}{{}} {cond_obj["operation"]} {{}} "
            querry = sql.SQL(querry).format(
                sql.Literal(cond_obj["rowA"]) if cond_help.is_row_A_Literal else sql.Identifier(cond_obj["rowA"]), 
                sql.Literal(cond_obj["rowB"]) if cond_help.is_row_B_Literal else sql.Identifier(cond_obj["rowB"])
            ).as_string(self.__connection)
        
        # Finalize
        querry = sql.SQL(querry)

        with self.__connection.cursor() as cursor:
            cursor.execute(querry)
            self.__connection.commit()
            return cursor.fetchall()




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
            TypeError: For incorrect argument type
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

        # Update Cache
        if tbl not in self.__row_cache:
            self.__add_cache(tbl)

        w_helper = _WhereHelper(bool(select_options.get("WHERE", False)), self.__row_cache[tbl], where["operation"], where["rowA"], where["rowB"])
        o_helper = _OrderByHelper(bool(select_options.get("ORDER_BY", False)), order_by["asc"])

        querry = self.__form_sel_querry(
            main            =   True,
            table           =   tbl,
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


    def delete_from(self, tbl: str, where: 'dict|None'=None):
        """Deletes from a specified table in the database

        Args:
            tbl (str): The name of the table
            where (dict|None, optional): The where clause of the querry if it exists. Defaults to None.

        Where dict format:
        ```
        # Will do rowA operation rowB
        {"operation": ">", "rowA": "name", "rowB": "name2"}
        ```
        """
        # Update Cache
        if tbl not in self.__row_cache:
            self.__add_cache(tbl)
        
        w_helper = _WhereHelper(bool(where), self.__row_cache[tbl], where["operation"], where["rowA"], where["rowB"])

        querry = self.__form_del_querry(w_helper)
        querry = querry.format(
            table          =   sql.Identifier(tbl),
            where_rowA     =   sql.Literal(where["rowA"]) if w_helper.is_row_A_Literal else sql.Identifier(where["rowA"]),
            where_rowB     =   sql.Literal(where["rowB"]) if w_helper.is_row_B_Literal else sql.Identifier(where["rowB"]),
        )

        with self.__connection.cursor() as cursor:
            cursor.execute(querry)
            self.__connection.commit()

    
    def insert_into(self, tbl: str, values:'list[str]', rows:'list[str]'=None):
        """Inserts specified values into specifed rows for a specified table in the database

        Args:
            tbl (str): The target table
            values (list[str]): A list of values to insert
            rows (list[str], optional): The rows to add. Defaults to None, when defaulted to None assumes all rows.

        Raises:
            TypeError: For incorrect argument types
            ValueError: For incorrect argument values
        """
        if type(values) != list:
            raise TypeError(f"{values}: not a list")
        elif len(values) == 0:
            raise TypeError(f"{values}: cannot be empty")
        
        # Update Cache
        if tbl not in self.__row_cache:
            self.__add_cache(tbl)

        if rows:
            if not all(row in self.__row_cache[tbl] for row in rows):
                raise ValueError(f"Not all rows in {rows} exist in the table {tbl}")
            use_rows = rows
        else:
            use_rows = self.__row_cache[tbl]

        if not len(use_rows) == len(values):
            raise ValueError(f"{values} and {use_rows} must be the same length")
        
        querry = self.__form_insert_querry(has_rows=bool(rows))
        querry = querry.format(
            table   =   sql.Identifier(tbl), 
            values  =   sql.SQL(",").join([sql.Literal(v) for v in values]), 
            rows    =   sql.SQL(",").join([sql.Identifier(r) for r in use_rows])
        )

        with self.__connection.cursor() as cursor:
            cursor.execute(querry)
            self.__connection.commit()
        



