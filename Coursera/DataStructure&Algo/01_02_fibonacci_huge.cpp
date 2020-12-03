#include <iostream>
#include <vector>

long long get_fibonacci_huge_naive(long long n, long long m) {
    if (n <= 1)
        return n;

    long long previous = 0;
    long long current  = 1;

    for (long long i = 0; i < n - 1; ++i) {
        long long tmp_previous = previous;
        previous = current;
        current = tmp_previous + current;
    }

    return current % m ;
}

long long get_fibo_huge_fast(long long n, long long m) {
    if (n > 1) {
        std::vector<long long> ve(n+1);
        ve[0] = 0;
        ve[1] = 1;
        for (long long i=2; i!=(n+1); i++) {
            ve[i] = ve[i-1] + ve[i-2];
        }
        return *ve.rbegin() % m ;
    }
    else {
        return n;
    }
}

int main() {
    long long n, m;
    std::cin >> n >> m;
    //std::cout << get_fibonacci_huge_naive(n, m) << '\n';
    std::cout << get_fibo_huge_fast(n, m) << "\n";
}
