class Animal:
    def __init__(self, name : str,age : int):
        self.name = name
        self.age =  age


class  Dog(Animal):
    def speaks(self):
        return f"{self.name} - {self.age}  years old"
    
animal =  Animal
dog = Dog("dog",10)
print(dog.speaks())