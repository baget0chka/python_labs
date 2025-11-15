#include <iostream>
#include <cmath>

void displayMenu() {
    std::cout << "=== CALCULATOR ===" << std::endl;
    std::cout << "1. Addition (+)" << std::endl;
    std::cout << "2. Subtraction (-)" << std::endl;
    std::cout << "3. Multiplication (*)" << std::endl;
    std::cout << "4. Division (/)" << std::endl;
    std::cout << "5. Power (^)" << std::endl;
    std::cout << "6. Exit" << std::endl;
    std::cout << "Choose operation: ";
}

void calculator() {
    int choice;
    float num1, num2, result;
    
    while (choice != 6){
        displayMenu();
        std::cin >> choice;
        
        switch (choice) {
            case 1:
                std::cout << "Enter first number: ";
                std::cin >> num1;
                std::cout << "Enter second number: ";
                std::cin >> num2;
                result = num1 + num2;
                std::cout << "Result: " << num1 << " + " << num2 << " = " << result << std::endl;
                break;
                
            case 2:
                std::cout << "Enter first number: ";
                std::cin >> num1;
                std::cout << "Enter second number: ";
                std::cin >> num2;
                result = num1 - num2;
                std::cout << "Result: " << num1 << " - " << num2 << " = " << result << std::endl;
                break;
                
            case 3:
                std::cout << "Enter first number: ";
                std::cin >> num1;
                std::cout << "Enter second number: ";
                std::cin >> num2;
                result = num1 * num2;
                std::cout << "Result: " << num1 << " * " << num2 << " = " << result << std::endl;
                break;
                
            case 4:
                std::cout << "Enter dividend: ";
                std::cin >> num1;
                std::cout << "Enter divisor: ";
                std::cin >> num2;
                if (num2 != 0) {
                    result = num1 / num2;
                    std::cout << "Result: " << num1 << " / " << num2 << " = " << result << std::endl;
                } 
                else {
                    std::cout << "Error! Division by zero is impossible." << std::endl;
                }
                break;
                
            case 5:
                std::cout << "Enter base: ";
                std::cin >> num1;
                std::cout << "Enter exponent: ";
                std::cin >> num2;
                result = std::pow(num1, num2);
                std::cout << "Result: " << num1 << " ^ " << num2 << " = " << result << std::endl;
                break;
            case 6:
                std::cout << "Goodbye!" << std::endl;
                break;
            default:
                std::cout << "Invalid choice! Please try again." << std::endl;
                break;
        }
        
        std::cout << std::endl;
    }
}

int main() {
    std::cout << "Welcome to the calculator!" << std::endl;
    calculator();
    
    return 0;
}