/*
Description: Used to swap 2 int without 3rd variable.
*/
#include <iostream>

inline void swap_xor (int& a, int& b) {
    b = a^b;
    a = a^b;
    b = a^b;
}

inline void swap_t (int& a, int& b) {
    a = b - a;
    b = b - a;
    a = a + b;
}

int main() {
    int a,b;
    std::cin >> a >> b;
    
    swap_xor(a,b);
    std::cout << a << " " << b << "\n";
    swap_t(a,b);
    std::cout << a << " " << b << "\n";
    return 0; 
}
