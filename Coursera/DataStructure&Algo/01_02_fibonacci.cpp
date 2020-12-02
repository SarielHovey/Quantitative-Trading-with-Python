#include <iostream>
#include <cassert>
#include <vector>

int fibonacci_naive(int n) {
    if (n <= 1)
        return n;

    return fibonacci_naive(n - 1) + fibonacci_naive(n - 2);
}

int fibonacci_fast(int n) {
    if (n > 1) {
        std::vector<int> ve(n+1);
        ve[0] = 0;
        ve[1] = 1;
        for (int i=2; i!=(n+1); i++) {
            ve[i] = ve[i-1] + ve[i-2];
        }
        return *ve.rbegin();
    }
    else if (n = 1) {
        return 1;
    }
    else {
        return n;
    }
}

void test_solution() {
    assert(fibonacci_fast(3) == 2);
    assert(fibonacci_fast(10) == 55);
    for (int n = 0; n < 20; ++n)
        assert(fibonacci_fast(n) == fibonacci_naive(n));
}

int main() {
    int n = 0;
    std::cin >> n;
    //std::cout << fibonacci_naive(n) << '\n';
    //test_solution();
    std::cout << fibonacci_fast(n) << '\n';
    return 0;
}
