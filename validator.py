import re

class Validator:
    @staticmethod
    def name_validator(name):
        numbers = re.findall(r"\d+", name)
        if not numbers and name[0] == name[0].upper():
            return True
        else:
            return False
        
    @staticmethod
    def phone_validator(phone):
        valid_phone = re.match(r"\d+", phone).string
        if phone == valid_phone and len(phone) == 11:
            return True
        else:
            return False
    
    @staticmethod
    def email_validator(email): return True
    
    @staticmethod
    def address_validator(address): return True