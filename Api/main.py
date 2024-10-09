import re
import string
from tinydb import TinyDB,where
from pathlib import Path

class User:

    DB = TinyDB(Path(__file__).resolve().parent / "db.json", indent=4)

    def __init__(self,first_name:str,last_name:str,phone_number:str='',address:str='') :
        self.first_name = first_name
        self.last_name = last_name
        self.phone_number = phone_number
        self.address = address


    def __repr__(self):
        return f"{self.first_name} {self.last_name}"
    
    
    @property
    def full_name(self):
        return f"{self.first_name} {self.last_name}"
    
    @property
    def db_instance(self):
        return User.DB.get((where('first_name')== self.first_name) & (where("last_name")== self.last_name))
    

    def __str__(self):
        return f"{self.first_name}\n{self.full_name}\n {self.phone_number}\n {self.address}"
    

    def _checks(self):
        self._check_name()
        self._check_phone_number()


    def _check_phone_number(self):
        phone_digits = re.sub(r"[+()\s]*","",self.phone_number)
        if len(phone_digits) < 10 or not phone_digits.isdigit():
            raise ValueError(f"Numero de telephone {self.phone_number} invalide.")
        
        
    def _check_name(self):
        if not(self.first_name and self.last_name):
            raise ValueError("Le nom et le prenom ne peuvent pas etre vide.")

        special_characters = string.punctuation + string.digits

        for character in self.first_name + self.last_name:
            if character in special_characters:
                raise ValueError(f"Nom Invalide {self.full_name}")
            
    def exists(self):
        return bool(self.db_instance)
    

    def delete(self)-> list[int]:
        if self.exists():
           return User.DB.remove(doc_ids= [self.db_instance.doc_id])
        return []

    def save(self,validate_data=False):
        if validate_data:
            self._checks()


        return User.DB.insert(self.__dict__)
    

def get_all_users():
    return [User(**user) for user in User.DB.all()]
        

if __name__== "__main__":

    laura = User('Laura','Nelson')
    print(laura.db_instance)
    # print(laura.exists())
    laura.delete()
