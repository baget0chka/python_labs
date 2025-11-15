#include <iostream>
#include <string>

class Animal {
protected:
    std::string name;
    std::string sound;

public:
    Animal(const std::string& animalName, const std::string& animalSound) {
        name = animalName;
        sound = animalSound;
    }

    virtual void makeSound() const {
        std::cout << name << " makes sound: " << sound << std::endl;
    }

    virtual void eat() const {
        std::cout << name << " is eating...\n";
    }

    virtual void sleep() const {
        std::cout << name << " is sleeping...\n";
    }

    std::string getName() const { 
        return name; 
    }
    std::string getSound() const { 
        return sound; 
    }

    void setName(const std::string& newName) { 
        name = newName; 
    }

    virtual void displayInfo() const {
        std::cout << "Animal: " << name << "\n";
    }
};

class Cat : public Animal {
private:
    std::string furColor;

public:
    Cat(const std::string& catName, const std::string& color = "gray"){
        furColor = color;
        name = catName;
        sound = "Mewow!";
    }

    void makeSound() const override {
        std::cout << name << " meows: " << sound << std::endl;
    }

    void eat() const override {
        std::cout << name << " eats fish and drinks milk\n";
    }

    void climbTree() const {
        std::cout << name << " climbs trees!\n";
    }

    void purr() const {
        std::cout << name << " purrs: purrrrr...\n";
    }

    void displayInfo() const override {
        std::cout << "Cat: " << name << ", fur color: " << furColor << "\n";
    }

    std::string getFurColor() const { 
        return furColor;
    }
};

class Dog : public Animal {
private:
    bool isTrained;

public:
    Dog(const std::string& dogName, bool trained = false){
        isTrained = trained;
        sound = "Woof!";
        name = dogName;
    }

    void makeSound() const override {
        std::cout << name << " barks: " << sound << std::endl;
    }

    void eat() const override {
        std::cout << name << " eats bones and dry food\n";
    }

    void fetch() const {
        std::cout << name << " fetches a stick!\n";
    }

    void train() {
        if (!isTrained) {
            isTrained = true;
            std::cout << name << " is now trained!\n";
        }
        else {
            std::cout << name << " is already trained!\n";
        }
    }

    void displayInfo() const override {
        std::string trained = (isTrained ? "yes" : "no");
        std::cout << "Dog: " << name << ", trained: " << trained << "\n";
    }

    bool getIsTrained() const { 
        return isTrained; 
    }
};

void animalShow(const Animal& animal) {
    animal.displayInfo();
    animal.makeSound();
    animal.eat();
    std::cout << "--------------------\n";
}

int main() {
    Cat cat("Whiskers", "orange");
    Dog dog("Buddy", false);

    std::cout << "=== Cats demonstration ===\n";
    cat.displayInfo();
    cat.makeSound();
    cat.eat();
    cat.purr();
    cat.climbTree();
    std::cout << "\n";

    std::cout << "=== Dogs demonstration ===\n";
    dog.displayInfo();
    dog.makeSound();
    dog.eat();
    dog.fetch();
    dog.train();
    dog.train();
    std::cout << "\n";

    std::cout << "=== Polymorphism demonstration ===\n";
    animalShow(cat);
    animalShow(dog);

    return 0;
}