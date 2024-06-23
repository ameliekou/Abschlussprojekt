import json
from datetime import datetime

class DB:
    def __init__(self) -> None:
        with open("person_db.json") as file:
            person_data = json.load(file)
            self.persons = {}
            for eintrag in person_data:
                p = Person(eintrag)
                self.persons[p.firstname + ", " +  p.lastname] = p
        
    def get_person_list(self):
        return self.persons.keys()
    
    def find_person_data_by_name(self, suchstring):
        return self.persons[suchstring]
    
    def load_by_id(self, ID):
        for person in self.persons.values():
            if person.id == ID:
                return person

class Person:    
    def __init__(self, person_dict) -> None:
        self.date_of_birth = person_dict["date_of_birth"]
        self.firstname = person_dict["firstname"]
        self.lastname = person_dict["lastname"]
        self.picture_path = person_dict["picture_path"]
        self.id = person_dict["id"]

    def calc_age(self):
        '''A function that calculates the age of a person based on the date of birth.'''

        today = datetime.today()
        age = today.year - self.date_of_birth
        
        return age


    def calc_max_heart_rate(self):
        '''A function that calculates the maximum heart rate of a person.'''

        age = self.calc_age()
        max_heart_rate = 220 - age

        return max_heart_rate


if __name__ == "__main__":
    print("This is a module with some functions to read the person data")
    persons = Person.load_person_data()
    person_names = Person.get_person_list(persons)
    person1 = Person(Person.find_person_data_by_name("Huber, Julian"))
    print(person1.calc_max_heart_rate())
    print(Person.load_by_id(1))
    