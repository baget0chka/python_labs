
def bubbleSort(arr):
	n = len(arr)
	for i in range(0, n - 1, 1):
		swapped = False
		for j in range(0, n - i - 1, 1):
			if arr[j] > arr[j + 1]:
				temp = arr[j]
				arr[j] = arr[j + 1]
				arr[j + 1] = temp
				swapped = True
		if not swapped:
			break

def shakerSort(arr):
	left = 0
	right = len(arr) - 1
	swapped = True
	
	while left < right and swapped:
		swapped = False
		
		for i in range(left, right, 1):
			if arr[i] > arr[i + 1]:
				temp = arr[i]
				arr[i] = arr[i + 1]
				arr[i + 1] = temp
				swapped = True
		right = right - 1
		
		for i in range(right, left, -1):
			if arr[i] < arr[i - 1]:
				temp = arr[i]
				arr[i] = arr[i - 1]
				arr[i - 1] = temp
				swapped = True
		left = left + 1

if __name__ == '__main__':
	print("=== Integer Sorting Demo ===" )
	
	data = [64, 34, 25, 12, 90]
	n1 = len(data)
	
	print("Before bubble sort: ", end='')
	for i in range(0, n1, 1):
		print(data[i] , " ", end='')
	print()
	
	bubbleSort(data)
	print("After bubble sort: ", end='')
	for i in range(0, n1, 1):
		print(data[i] , " ", end='')
	print()
	
	data2 = [90, 64, 34, 25, 12]
	n2 = len(data2)
	print("\nBefore shaker sort: ", end='')
	for i in range(0, n2, 1):
		print(data2[i] , " ", end='')
	print()
	
	shakerSort(data2)
	print("After shaker sort: ", end='')
	for i in range(0, n2, 1):
		print(data2[i] , " ", end='')
	print()
	
