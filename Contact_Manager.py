from contact_manager_interface import Window
import json
import re
from mysql_handler import Mysql_Handler
from contact_logger import contact_logger

class Contact_Manager(Mysql_Handler):
    def __init__(self, user, host, password, logger_name, logger_file_name, conosole_format, file_format):
        super(Contact_Manager, self).__init__(user, host, password)
        self.contacts = {}  
        self.contact_logger = contact_logger(logger_name,
                                            logger_file_name,
                                            conosole_format,
                                            file_format)
    
        try:
            self.contact_logger.debug("loading contacts file ...".upper())
            self.load_contacts()
            self.contact_logger.debug("completed".upper())
        except FileNotFoundError:
            self.contact_logger.error("file doesn't exist".upper())
            self.save_contact()
            self.contact_logger.info("Create new file".upper())

    def load_contacts(self):
        with open("contact_manager.json", "r") as f:
            self.contacts = json.loads(f.read())

    def save_contact(self):
        self.connect_database(database_name="Contact_Manager")
        self.create_table(table_name="contacts")
        with open("contact_manager.json", "w") as f:
            f.write(json.dumps(self.contacts))

    def add_contact(self, name, phone, email=None,  address=None):
        if name in self.contacts:
            self.contact_logger.warning(f"{name} EXIST IN THE CONTACTS LIST")
        else:
            self.contacts[name] = {
                "phone" : phone,
                "email" : email,
                "address" : address
            }
        self.contact_logger.info(f"{name} HAS BEEN CREATED")
        self.save_contact()
        self.add_data(name, phone, email, address, table_name="contacts")
        self.contact_logger.info(f"{name} SAVED")

    def remove_contact(self, name):
        if name in self.contacts:
            del self.contacts[name]
            self.save_contact()
            self.contact_logger.info("removing contact".upper())
        else:
            self.contact_logger.warning(f"{name} IS NOT IN THE CONTACT LIST")

        self.remove_data("contacts", name=name)
        
    # def search_contact(self, value):
    #     result = []
    #     for key in self.contacts:
    #         if value in key:
    #             result.append(key)
    #     if result:
    #         for find in result:
    #             self.contact_logger.debug(f"{find} : phone : {self.contacts[find]['phone']} - email : {self.contacts[find]['email']} - address : {self.contacts[find]['address']}")
    #     else:
    #         self.contact_logger.warning("Doesn't find anything")
    
    # def show_contacts(self):
    #     i = 1
    #     for name, contact in self.contacts.items():
    #         self.contact_logger.debug(f"{i}.{name} : phone : {contact['phone']} - email : {contact['email']} - address : {contact['address']}")
    #         i += 1
            
    @staticmethod
    def get_input(text, force=False):
        value = input(text)
        if force and not value:
            return Contact_Manager.get_input(text, force)
        return value if value else None
    
    def operation(self):
        window = Window("1.Add Contact", "2.Remove Contact", "3.Show All Contact", "4.Search Contact", "5.Exit", total_button=5)
        window.mainloop()

        try:
            name = window.name
            phone = window.phone
            email = window.email
            address = window.address
        except:
            invalid_input = "contact input doesnt exist"
            self.contact_logger.debug(invalid_input)
            try:
                remove_name_text = window.remove_name_text
            except:
                invalid_input = "remove contact input doesnt exist" 
                self.contact_logger.debug(invalid_input)
        try:
            self.add_contact(name, phone, email, address)
        except:
            try:
                self.remove_contact(remove_name_text)
            except:
                self.contact_logger.error("Something went wrong")
        # self.contact_logger.debug(text)
        # user_choice = int(input("Enter you'r choice : "))
        # if user_choice == 1:
        #     name = self.get_input(text="Contact Name : ", force=True)
        #     if self.name_validator(name):
        #         phone = self.get_input(text="Contact Phone : ", force=True)
        #         if self.phone_validator(phone):
        #             email = self.get_input(text="Contact email : ")
        #             if self.email_validator(email):
        #                 address = self.get_input(text="Contact address : ")
        #                 if self.address_validator(address):
        #                     self.add_contact(name, phone, email, address)
        #                     self.back_to_operation()
        #                 else:
        #                     self.contact_logger.debug("Not Valid Address")
        #             else:
        #                 self.contact_logger.debug("Not Valid Email")
        #         else:
        #             self.contact_logger.debug("Not Valid Phone Number")
        #     else:
        #         self.contact_logger.debug("Must Start With UppperCase And It Has Not Numbers")
        # elif user_choice == 2:
        #     name = self.get_input(text="Contact Name (for Removing) : ")
        #     self.remove_contact(name)
        #     self.back_to_operation()
        # elif user_choice == 3:
        #     query = self.get_input(text="Search : ")
        #     self.search_contact(value=query)
        #     self.back_to_operation()
        # elif user_choice == 4:
        #     self.show_contacts()
        #     self.back_to_operation()
        # elif user_choice == 5:
        #     print("Closing Program")
        #     exit()

    def back_to_operation(self):
        value = self.get_input(text="Enter 'q' for exit and other keys to back to the menu : ")
        if value == "q":
            exit()
        else:
            self.operation()



if __name__ == "__main__":
    user = "root"
    password = "."
    host = "localhost"

    logger_name = "Contact_Manager_Logger"
    logger_file_name = "contact.log"
    conosole_format = "%(levelname)s | %(message)s"
    file_format = "%(asctime)s | %(levelname)s | %(message)s"
    contact_manager = Contact_Manager(user, host, password, logger_name, logger_file_name, conosole_format, file_format)
    contact_manager.operation()