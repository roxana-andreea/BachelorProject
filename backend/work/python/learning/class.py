#!/usr/local/bin/python3

class Person:
    def __init__(self, age):
        self.age = age

class PersonWithAccessors:
    def __init__(self, age):
        self._age = age

    def get_age(self):
        return self._age

    def set_age(self, age):
        if 18 <= age <= 99:
            self._age = age
        else:
            raise ValueError("Age not valid")

class PersonPythonic:
    def __init__(self, age):
        self._age = age

    @property
    def age(self):
        return  self._age

    @age.setter
    def age(self, age):
        if 18<= age <= 99:
            self._age = age
        else:
            raise ValueError("age invalid")

person = PersonPythonic(200)
print(person.age)
person.age = 42
print(person.age)
