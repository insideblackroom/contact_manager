import json
import tkinter as tk
import tkinter.messagebox as msgbox
from validator import Validator
class Window(tk.Tk):
    def __init__(self, *args,  total_button,):
        super(Window, self).__init__()
        self.title = "Contact Manager"
        self.positionfrom("program")

        self.__name_text = tk.StringVar()
        self.__phone_text = tk.StringVar()
        self.__email_text = tk.StringVar()
        self.__address_text = tk.StringVar()

        self.__remove_name = tk.StringVar()
        self.__search_text = tk.StringVar()

        for i in range(total_button):
            self.button = tk.Button(self, text=args[i], bg="black", fg="white")
            self.button.grid(row=0, column=i, ipadx=100, ipady=25)
            if "add" in args[i].lower():
                self.button.configure(command=self.add_contact)
            elif "remove" in args[i].lower():
                self.button.configure(command=self.remove_contact)
            elif "show" in args[i].lower():
                self.button.configure(command=self.show_contact)
            elif "search" in args[i].lower():
                self.button.configure(command=self.seach_contact)
            elif "exit" in args[i].lower():
                self.button.configure(command=self.exit)

    def add_contact(self):
        self.name_label = tk.Label(self, text="name: ")
        self.name_label.grid(row=1, column=0, pady=(23,30))
        self.name_entry = tk.Entry(self, textvariable=self.__name_text, justify="center")
        self.name_entry.grid(row=2, column=0, pady=(23,30))

        self.phone_label = tk.Label(self, text="phone number: ")
        self.phone_label.grid(row=3, column=0, pady=(23,30))
        self.phon_entry = tk.Entry(self, textvariable=self.__phone_text, justify='center')
        self.phon_entry.grid(row=4, column=0, pady=(23,30))

        self.email_label = tk.Label(self, text="email: ")
        self.email_label.grid(row=5, column=0, pady=(23,30))
        self.email_entry = tk.Entry(self, textvariable=self.__email_text, justify="center")
        self.email_entry.grid(row=6, column=0, pady=(23,30))

        self.address_label = tk.Label(self, text="Address: ")
        self.address_label.grid(row=7, column=0, pady=(23,30))
        self.address_entry = tk.Entry(self, textvariable=self.__address_text, justify="center")
        self.address_entry.grid(row=8, column=0, pady=(23,30))

        self.save = tk.Button(self, text="Save", command=self.submit_contact)
        self.save.grid(row=9, column=0, pady=(23,30))

    def submit_contact(self):
        message = f"name : {self.__name_text.get()} \n phone : {self.__phone_text.get()} \n email : {self.__email_text.get()} \n address : {self.__address_text.get()}"
        if Validator.name_validator(name=self.__name_text.get()):
            self.name = self.__name_text.get()
            if Validator.phone_validator(phone=self.__phone_text.get()):
                self.phone = self.__phone_text.get()
                if Validator.email_validator(email=self.__email_text.get()):
                    self.email = self.__email_text.get()
                    if Validator.address_validator(address=self.__address_text.get()):
                        self.address = self.__address_text.get()
                        if msgbox.askokcancel("confirmation", message):
                            msgbox.showinfo("completed", "ALL DONE. Click on Exit")
                            return True
                    else:
                        msgbox.showwarning("WARNING", "address is incorrect!")
                else:
                    msgbox.showwarning("WARNING", "email is incorrect!")
            else:
                msgbox.showwarning("WARNING", "phone is incorrect")
        else:
            msgbox.showwarning("WARNING", "name is incorrect")
            


    def remove_contact(self):
        self.name_label2 = tk.Label(self, text="name:")
        self.name_label2.grid(row=1, column=1)
        self.name_entry = tk.Entry(self, textvariable=self.__remove_name)
        self.name_entry.grid(row=2, column=1)

        self.save = tk.Button(self, text="Remove", command=self.submit_remove_contact)
        self.save.grid(row=3, column=1, pady=(23,30))

    def submit_remove_contact(self):
        confirmation = msgbox.askyesno(title="confirmation", message="Are You Sure?")
        if confirmation:
            self.remove_name_text = self.__remove_name.get()
            msgbox.showinfo("Announcement", "Removing completed after close the program")

    def show_contact(self):
        self.read_contacts()
        i = 1
        for name,contact in self.contacts.items():
            contact_info = f"name : {name} \nphone : {contact["phone"]} \nEmail : {contact["email"]} \nAddress : {contact["address"]}\n"
            tk.Label(self, text=contact_info).grid(row=i, column=2)
            i += 1

    def seach_contact(self):
        self.search_label = tk.Label(self, text="Search:")
        self.search_label.grid(row=1, column=3, pady=(23,30))
        self.search_entry = tk.Entry(self, textvariable=self.__search_text)
        self.search_entry.grid(row=2, column=3, pady=(23,30))
        self.search_button = tk.Button(self, text="Find contact", command=self.searching)
        self.search_button.grid(row=3, column=3, pady=(23,30))

    def searching(self):
        self.read_contacts()
        self.search_text = self.__search_text
        results = []
        for key in self.contacts:
            if self.search_text.get().lower() in key.lower():
                results.append(key)
        if results:
            i = 4
            for find in results:
                text = f"name : {find}\nphone : {self.contacts[find]["phone"]}\nEmail : {self.contacts[find]["email"]}\nAddress : {self.contacts[find]["address"]}\n"
                tk.Label(self, text=text).grid(row=i, column=3)
                i += 1

    def read_contacts(self):
        with open("contact_manager.json", "r") as contacts_file:
            self.contacts = json.loads(contacts_file.read())

    def exit(self):
        self.exit_button = tk.Button(self, text="Close And Save Change", command=self.destroy)
        self.exit_button.grid(row=1, column=4, pady=(23,50))

    def return_error(self, value):
        message = f"invalid input in '{value}', check it again"
        msgbox.showwarning("warning", message)

if __name__ == "__main__":
    window = Window("1.Add Contact", "2.Remove Contact", "3.Show All Contact", "4.Search Contact", "5.Exit", total_button=5)
    window.mainloop()