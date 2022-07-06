import sqlite3


class Db:
    """
    class DB-manager
    """
    def __init__(self):
        self.conn = sqlite3.connect('contacts.db')
        self.cur = self.conn.cursor()

    def __del__(self):
        self.conn.close()
        self.cur.close()

    def create_tables(self):
        """
        function create tables to DB
        """

        try:
            # Create phones
            self.cur.execute('''
            CREATE TABLE phones
            (Id INTEGER PRIMARY KEY,
            ContactName varchar(255) NOT NULL, 
            Phone varchar(20) UNIQUE)
            ''')
            self.conn.commit()


            # Create other tables
            # get_cursor().execute('''
            # ''')
            # self.conn.commit()

        finally:
            # Close the connection
            self.cur.close()
            self.conn.close()
