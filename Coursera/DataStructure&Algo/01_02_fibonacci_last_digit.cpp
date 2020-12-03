#include <iostream>
#include <vector>

int get_fibonacci_last_digit_naive(int n) {
    if (n <= 1)
        return n;

    int previous = 0;
    int current  = 1;

    for (int i = 0; i < n - 1; ++i) {
        int tmp_previous = previous;
        previous = current;
        current = tmp_previous + current;
    }

    return current % 10;
}

int get_fibo_last_digit_fast(int n) {
    if (n > 1) {
        std::vector<int> ve(n+1);
        ve[0] = 0;
        ve[1] = 1;
        for (int i=2; i!=(n+1); i++) {
            ve[i] = (ve[i-1] % 10 + ve[i-2] % 10) % 10;
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

int main() {
    int n;
    std::cin >> n;
    int c = get_fibo_last_digit_fast(n);
    std::cout << c << '\n';
    }
// http://fusharblog.com/solving-linear-recurrence-for-programming-contest/
