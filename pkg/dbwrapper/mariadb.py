import pymysql
class MariaDBWrapper:
    def __init__(self, db_host, db_user, db_passwd, db_name):

        self.conn = None
        self.db_host_ = db_host
        self.db_user_ = db_user
        self.db_passwd_ = db_passwd
        self.db_name_ = db_name

        self.conn = self.init_db()
        self.conn_status = True if self.conn else False
    
    @staticmethod
    def apply_field(desc, col, row, sql, first_row = False, sql_type = "insert"):
        if desc[col] in ['int', 'float'] or 'int' in desc[col]:
            if sql_type == "insert":
                sql += f", {row[col]}" if not first_row else f"{row[col]}"
            else:
                sql += f", {col} = {row[col]}" if not first_row else f"{col} = {row[col]}"
        else:
            if sql_type == "insert":
                sql += f", '{row[col]}'" if not first_row else f"'{row[col]}'"
            else:
                sql += f", {col} = '{row[col]}'" if not first_row else f"{col} = '{row[col]}'"
        return sql

    def init_db(self):
        try:
            conn = pymysql.connect(host=self.db_host_
                               , user=self.db_user_ 
                               , password=self.db_passwd_
                               , db=self.db_name_)
            return conn
        except Exception as e:
            return None
        
    def select(self, sql):
        cursor = None
        if self.conn_status:
            cursor = self.conn.cursor(pymysql.cursors.DictCursor)
        else:
            return None
        cursor.execute(sql)
        return cursor.fetchall()

    def insert(self, table, df, key = None):
        cursor = None
        if self.conn_status:
            cursor = self.conn.cursor(pymysql.cursors.DictCursor)
        else:
            return None
        # desc query
        sql = f"DESC {table}"
        cursor.execute(sql)
        desc = {}
        # check column
        for col_info in cursor.fetchall():
            desc[col_info['Field']] = col_info['Type']

        # execute insert table from df
        for i, row in df.iterrows():
            try:
                sql = f"INSERT INTO {table} "
                sql += "("
                for j, col in enumerate(df.columns):
                    if j == 0:
                        sql += col
                    else:
                        sql += f", {col}"
                sql += ") "
                sql += "VALUES ("
                for j, col in enumerate(df.columns):
                    sql = MariaDBWrapper.apply_field(
                        desc, col, row, sql, first_row= (j == 0))
                sql += ")"
                cursor.execute(sql)
            except Exception as e:
                if 'Duplicate entry' in str(e):
                    self.update(table, df.iloc[[i]], key = key)
                pass

        self.conn.commit()
    
    def update(self, table, df, key = None):
        cursor = None
        if self.conn_status:
            cursor = self.conn.cursor(pymysql.cursors.DictCursor)
        else:
            return None
        # desc query
        sql = f"DESC {table}"
        cursor.execute(sql)
        desc = {}
        # check column
        for col_info in cursor.fetchall():
            desc[col_info['Field']] = col_info['Type']

        # execute insert table from df
        for i, row in df.iterrows():
            try:
                sql = f"UPDATE {table} SET "
                for j, col in enumerate(df.columns):
                    sql = MariaDBWrapper.apply_field(
                        desc, col, row, sql, first_row= (j == 0), sql_type = "update")
                if key == None:
                    if desc[df.columns[0]] in ['int', 'float'] or 'int' in desc[df.columns[0]]:
                        sql += f" WHERE {df.columns[0]} = {row[df.columns[0]]}"
                    else:
                        sql += f" WHERE {df.columns[0]} = '{row[df.columns[0]]}'"
                else:
                    if desc[key] in ['int', 'float'] or 'int' in desc[key]:
                        sql += f" WHERE {key} = {row[key]}"
                    else:
                        sql += f" WHERE {key} = '{row[key]}'"
                cursor.execute(sql)
            except Exception as e:
                print(e)
                pass
        self.conn.commit()