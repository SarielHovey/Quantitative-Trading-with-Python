#include <iostream>
#include <vector>

long long get_fibonacci_huge_naive(long long n, long long m) {
    if (n <= 1)
        return n;

    long long previous = 0;
    long long current  = 1;

    for (long long i = 0; i != n - 1; ++i) {
        long long tmp_previous = previous % m;
        previous = current % m;
        current = (tmp_previous + current) % m;
    }

    return current;
}

long long unsigned get_fibo_huge_fast(long long unsigned n, long long unsigned m) {
    if (n > 1) {
        std::vector<long long unsigned> ve(n+1);
        ve[0] = 0;
        ve[1] = 1;
        for (long long unsigned i=2; i!=(n+1); i++) {
            ve[i] = (ve[i-1] % m + ve[i-2] % m) % m;
        }
        return *ve.rbegin();
    }
    else {
        return n;
    }
}

int main() {
    long long unsigned n, m;
    std::cin >> n >> m;
    //std::cout << get_fibonacci_huge_naive(n, m) << '\n';
    std::cout << get_fibo_huge_fast(n, m) << "\n";
}
