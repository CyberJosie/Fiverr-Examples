import sqlite3

class DBManager:

    def __init__(self, db_name="content.db"):
        self.database_name = db_name
        self.sql = self.connect()

    # Return Value -> ( bool(success), list(any_output), str(any_err) )
    def execute(self, command, commit=False):
        errmsg = ""
        try:
            rows = self.sql.cursor().execute(command).fetchall()
            if commit:
                self.sql.commit()
            
            return True, list(rows), ""
        except sqlite3.Error as er:
            errmsg = ' '.join(er.args)
            return False, [], errmsg

    
    # Creates the table if it doesnt exist "ensure" lol
    def ensure_content_table(self, table_name="content"):
        table_statement = f"""CREATE TABLE IF NOT EXISTS {table_name.lower()}(
id INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
product_name TEXT,
product_price TEXT,
product_link TEXT,
section varchar(32),
image_link TEXT);"""

        is_ok, _, err = self.execute(command=table_statement, commit=True)
        if is_ok:
            return True
        else:
            print(err)
            return False
    
    def add_product(self, name, price, link, img_link, section, table="content"):
        sql_statement = f"""INSERT INTO {table.lower()} (product_name, product_price, product_link, image_link, section) VALUES (\"{name}\",\"{price}\",\"{link}\",\"{img_link}\",\"{section}\");"""
        is_ok, out, err = self.execute(command=sql_statement, commit=True)
        if is_ok:
            print(out)
            return True
        else:
            print(err)
            return False

    def connect(self):
        try:
            return sqlite3.connect(self.database_name)
        except sqlite3.Error as er:
            err = ' '.join(er.args) + f"\nException class: {er.__class__}"
            print(err)
            return None
