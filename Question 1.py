from tkinter import *
from tkinter import ttk

# Define the Animal, Dog, and Cat classes
class Animal:
    def __init__(self, name):
        self.name = name

    def eat(self):
        # Polymorphism: each subclass of Animal can have its own implementation of this method
        pass

class Dog(Animal):
    def eat(self):
        return "{} eats bones".format(self.name)

class Cat(Animal):
    def eat(self):
        return "{} eats fish".format(self.name)

# Define the Pet, DogPet, and CatPet classes
class Pet:
    def __init__(self, name, animal_cls):
        self.name = name
        # Encapsulation: the Pet class doesn't need to know the details of the Animal class, it just creates an instance of it
        self.animal = animal_cls(name)

    def feed(self):
        # Encapsulation: the Pet class uses the eat method of its animal instance, but doesn't need to know how it's implemented
        return self.animal.eat()

    def speak(self):
        # Polymorphism: each subclass of Pet must implement its own speak method
        return "This pet cannot speak"

class DogPet(Pet):
    def __init__(self, name):
        super().__init__(name, Dog)

    def speak(self):
        return "Woof!"

class CatPet(Pet):
    def __init__(self, name):
        super().__init__(name, Cat)

    def speak(self):
        return "Meow!"

# Define the Application class
class Application(Frame):
    def __init__(self, master=None):
        super().__init__(master)
        self.master = master
        self.master.title("Pet Manager")

        self.pets = []

        self.name_var = StringVar()
        self.animal_var = StringVar()

        animal_choices = ["Dog", "Cat"]

        self.name_label = ttk.Label(self, text="Name:")
        self.name_entry = ttk.Entry(self, textvariable=self.name_var)

        self.animal_label = ttk.Label(self, text="Animal:")
        self.animal_dropdown = ttk.Combobox(self, textvariable=self.animal_var, values=animal_choices)

        self.add_pet_button = ttk.Button(self, text="Add Pet", command=self.add_pet)
        self.feed_button = ttk.Button(self, text="Feed", command=self.feed_all)
        self.speak_button = ttk.Button(self, text="Speak", command=self.speak_all)
        self.clear_button = ttk.Button(self, text="Clear", command=self.clear_entries)

        self.output_text = Text(self, width=50, height=10)

        self.name_label.grid(row=0, column=0)
        self.name_entry.grid(row=0, column=1)
        self.animal_label.grid(row=1, column=0)
        self.animal_dropdown.grid(row=1, column=1)
        self.add_pet_button.grid(row=1, column=2)
        self.feed_button.grid(row=2, column=0)
        self.speak_button.grid(row=2, column=1)
        self.clear_button.grid(row=2, column=2)
        self.output_text.grid(row=3, column=0, columnspan=3)

        self.pack()

    def add_pet(self):
        # Encapsulation: the Application class only knows about Pets and the types of animals they can have
        name = self.name_var.get()
        animal_type = self.animal_var.get()

        if animal_type == "Dog":
            # Multiple inheritance: the DogPet class inherits from both Pet and Dog
            pet_obj = DogPet(name)
            self.pets.append(pet_obj)
        elif animal_type == "Cat":
            # Multiple inheritance: the CatPet class inherits from both Pet and Cat
            pet_obj = CatPet(name)
            self.pets.append(pet_obj)

        self.clear_entries()

    def feed_all(self):
        self.output_text.delete(1.0, END)
        for pet in self.pets:
            # Encapsulation: the Application class doesn't care about how pets are being fed, it just calls the feed method
            feed_text = pet.feed()
            self.output_text.insert(END, "{}\n".format(feed_text))

    def speak_all(self):
        self.output_text.delete(1.0, END)
        for pet in self.pets:
            # Encapsulation: the Application class doesn't care about how pets speak, it just calls the speak method
            speak_text = pet.speak()
            self.output_text.insert(END, "{}\n".format(speak_text))

    def clear_entries(self):
        self.name_var.set("")
        self.animal_var.set("")
        self.name_entry.focus()

# Create the main window and start the application
if __name__ == '__main__':
    root = Tk()
    app = Application(master=root)
    app.mainloop()