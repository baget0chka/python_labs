
def displayMenu():
	print("=== CALCULATOR ===" )
	print("1. Addition (+)" )
	print("2. Subtraction (-)" )
	print("3. Multiplication (*)" )
	print("4. Division (/)" )
	print("5. Power (^)" )
	print("6. Exit" )
	print("Choose operation: ", end='')

def calculator():
	choice = 0
	num1 = 0
	num2 = 0
	result = 0
	
	while choice != 6:
		displayMenu()
		choice = float(input())
		
		match choice:
			case 1:
				print("Enter first number: ", end='')
				num1 = float(input())
				print("Enter second number: ", end='')
				num2 = float(input())
				result = num1 + num2
				print("Result: " , num1 , " + " , num2 , " = " , result )
			
			case 2:
				print("Enter first number: ", end='')
				num1 = float(input())
				print("Enter second number: ", end='')
				num2 = float(input())
				result = num1 - num2
				print("Result: " , num1 , " - " , num2 , " = " , result )
			
			case 3:
				print("Enter first number: ", end='')
				num1 = float(input())
				print("Enter second number: ", end='')
				num2 = float(input())
				result = num1 * num2
				print("Result: " , num1 , " * " , num2 , " = " , result )
			
			case 4:
				print("Enter dividend: ", end='')
				num1 = float(input())
				print("Enter divisor: ", end='')
				num2 = float(input())
				if num2 != 0:
					result = num1 / num2
					print("Result: " , num1 , " / " , num2 , " = " , result )
				else:
					print("Error! Division by zero is impossible." )
			
			case 5:
				print("Enter base: ", end='')
				num1 = float(input())
				print("Enter exponent: ", end='')
				num2 = float(input())
				result = pow(num1, num2)
				print("Result: " , num1 , " ^ " , num2 , " = " , result )
			case 6:
				print("Goodbye!" )
			case _:
				print("Invalid choice! Please try again." )
		
		print()

if __name__ == '__main__':
	print("Welcome to the calculator!" )
	calculator()
	
