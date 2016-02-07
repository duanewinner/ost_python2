#!/usr/bin/python3

class Pet(object):

    def __init__(self, name, species, age):
        self.name = name
        self.species = species
        self.age = age

    def getName(self):
        return self.name

    def getSpecies(self):
        return self.species

    def getAge(self):
        return self.age

    def __str__(self):
        return "%s is a %s." % (self.name, self.species)


dog1=Pet("Rosa","dog",12)

print dog1
print dog1.getName()
print dog1.getAge()

