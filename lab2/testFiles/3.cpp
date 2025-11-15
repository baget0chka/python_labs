#include <iostream>
#include <vector>
#include <string>

template<typename T>
void bubbleSort(std::vector<T>& arr) {
    int n = arr.size();
    for (int i = 0; i < n - 1; i++) {
        bool swapped = false;
        for (int j = 0; j < n - i - 1; j++) {
            if (arr[j] > arr[j + 1]) {
                T temp = arr[j];
                arr[j] = arr[j + 1];
                arr[j + 1] = temp;
                swapped = true;
            }
        }
        if (!swapped) {
            break;
        }
    }
}

template<typename T>
void shakerSort(std::vector<T>& arr) {
    int left = 0;
    int right = arr.size() - 1;
    bool swapped = true;
    
    while (left < right && swapped) {
        swapped = false;
        
        for (int i = left; i < right; i++) {
            if (arr[i] > arr[i + 1]) {
                T temp = arr[i];
                arr[i] = arr[i + 1];
                arr[i + 1] = temp;
                swapped = true;
            }
        }
        right = right - 1;
        
        for (int i = right; i > left; i--) {
            if (arr[i] < arr[i - 1]) {
                T temp = arr[i];
                arr[i] = arr[i - 1];
                arr[i - 1] = temp;
                swapped = true;
            }
        }
        left = left + 1;
    }
}

int main() {
    std::cout << "=== Integer Sorting Demo ===" << std::endl;
    
    std::vector<int> data = {64, 34, 25, 12, 90};
    int n1 = data.size();
    
    std::cout << "Before bubble sort: ";
    for (int i = 0; i < n1; i++) {
        std::cout << data[i] << " ";
    }
    std::cout << std::endl;
    
    bubbleSort(data);
    std::cout << "After bubble sort: ";
    for (int i = 0; i < n1; i++) {
        std::cout << data[i] << " ";
    }
    std::cout << std::endl;
    
    std::vector<int> data2 = {90, 64, 34, 25, 12};
    int n2 = data2.size();
    std::cout << "\nBefore shaker sort: ";
    for (int i = 0; i < n2; i++) {
        std::cout << data2[i] << " ";
    }
    std::cout << std::endl;
    
    shakerSort(data2);
    std::cout << "After shaker sort: ";
    for (int i = 0; i < n2; i++) {
        std::cout << data2[i] << " ";
    }
    std::cout << std::endl;
    
    return 0;
}