
class Animal:
	_name = ''
	_sound = ''
	
	def __init__(self, animalName, animalSound):
		self._name = animalName
		self._sound = animalSound
	
	def makeSound(self):
		print(self._name, " makes sound: " ,self._sound)
	
	def eat(self):
		print(self._name, " is eating...\n", end='')
	
	def sleep(self):
		print(self._name, " is sleeping...\n", end='')
	
	def getName(self):
		return self._name
	def getSound(self):
		return self._sound
	
	def setName(self, newName):
		self._name = newName
	
	def displayInfo(self):
		print("Animal: " ,self._name, "\n", end='')

class Cat(Animal):
	__furColor = ''
	
	def __init__(self, catName, color = "gray"):
		self.__furColor = color
		self._name = catName
		self._sound = "Mewow!"
	
	def makeSound(self):
		print(self._name, " meows: " ,self._sound)
	
	def eat(self):
		print(self._name, " eats fish and drinks milk\n", end='')
	
	def climbTree(self):
		print(self._name, " climbs trees!\n", end='')
	
	def purr(self):
		print(self._name, " purrs: purrrrr...\n", end='')
	
	def displayInfo(self):
		print("Cat: " ,self._name, ", fur color: " ,self.__furColor, "\n", end='')
	
	def getFurColor(self):
		return self.__furColor

class Dog(Animal):
	__isTrained = False
	
	def __init__(self, dogName, trained = False):
		self.__isTrained = trained
		self._sound = "Woof!"
		self._name = dogName
	
	def makeSound(self):
		print(self._name, " barks: " ,self._sound)
	
	def eat(self):
		print(self._name, " eats bones and dry food\n", end='')
	
	def fetch(self):
		print(self._name, " fetches a stick!\n", end='')
	
	def train(self):
		if  not self.__isTrained:
			self.__isTrained = True
			print(self._name, " is now trained!\n", end='')
		else:
			print(self._name, " is already trained!\n", end='')
	
	def displayInfo(self):
		trained = {"yes" if self.__isTrained else "no"}
		print("Dog: " ,self._name, ", trained: " , trained , "\n", end='')
	
	def getIsTrained(self):
		return self.__isTrained

def animalShow(animal):
	animal.displayInfo()
	animal.makeSound()
	animal.eat()
	print("--------------------\n", end='')

if __name__ == '__main__':
	cat = Cat("Whiskers", "orange")
	dog = Dog("Buddy", False)
	
	print("=== Cats demonstration ===\n", end='')
	cat.displayInfo()
	cat.makeSound()
	cat.eat()
	cat.purr()
	cat.climbTree()
	print("\n", end='')
	
	print("=== Dogs demonstration ===\n", end='')
	dog.displayInfo()
	dog.makeSound()
	dog.eat()
	dog.fetch()
	dog.train()
	dog.train()
	print("\n", end='')
	
	print("=== Polymorphism demonstration ===\n", end='')
	animalShow(cat)
	animalShow(dog)
	
