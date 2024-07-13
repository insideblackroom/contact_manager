from contact_logger import contact_logger
from mysql import connector

class Mysql_Handler:
    def __init__(self, user, host, password):
        self.user = user
        self.host = host
        self.password = password
        self.mysql_logger = contact_logger(logger_name="Mysql_Handler_Logger",
                                            logger_file_name="mysql_handler.log",
                                            conosole_format_string="%(levelname)s | %(message)s",
                                            file_format_string="%(asctime)s | %(levelname)s | %(message)s")

        try:
            self.cnx = connector.connect(user=self.user, host=self.host, password=self.password)
            self.mysql_logger.debug("connection is satisfied".upper())
        except Exception as e:
            self.mysql_logger.error("something is wrong or have a trouble ----> %s" % e)

        self.cursor = self.cnx.cursor()

    def connect_database(self, database_name):
        if not database_name:
            raise ValueError("database name can't be empty")
        
        try:
            self.cnx.database = database_name
        except connector.errors.ProgrammingError as e:
            self.mysql_logger.error(f"{e}")
        
    def create_table(self, table_name):
        try:
            self.cursor.execute(f"SHOW TABLES LIKE '{table_name}'")
            searched_table = self.cursor.fetchone()
            if searched_table:
                self.mysql_logger.info("'{0}' Table is already exist".format(table_name))
            else:
                self.cursor.execute(f"""CREATE TABLE {table_name}
                                     (
                                    name VARCHAR(255) NOT NULL, 
                                    phone VARCHAR(255), 
                                    email VARCHAR(255), 
                                    address VARCHAR(255)
                                    )""".strip())
        except Exception as e:
            self.mysql_logger.error(f"{e}")

    def add_data(self, *args, table_name):
        self.cursor.execute(f"INSERT INTO {table_name} VALUES ('{args[0]}', '{args[1]}', '{args[2]}', '{args[3]}')")
        self.cnx.commit()

    def remove_data(self, table_name, name):
        self.cursor.execute(f"DELETE FROM {table_name} WHERE name='{name}'")
        self.cnx.commit()

if __name__ == "__main__":    
    ms = Mysql_Handler("root", "localhost", ".")
    ms.connect_database("contact_manager")
    ms.add_data("opre", "0910204", "asdasafas", "fajianfias", table_name="contacts")