#include <iostream>
#include <set>

int gcd_naive(int a, int b) {
  int current_gcd = 1;
  for (int d = 2; d <= a && d <= b; d++) {
    if (a % d == 0 && b % d == 0) {
      if (d > current_gcd) {
        current_gcd = d;
      }
    }
  }
  return current_gcd;
}

int gcd_fast(int a, int b) {
    std::multiset<int> ss;
    ss.insert(a);
    ss.insert(b);
    while (*ss.begin() != 0) {
        b = (*ss.rbegin()) % *(ss.begin());
        a = *ss.begin();
        ss.clear();
        ss.insert(a);
        ss.insert(b);
        }
    return *ss.rbegin();
    }
    

int main() {
  int a, b;
  std::cin >> a >> b;
  std::cout << gcd_fast(a, b) << std::endl;
  return 0;
}
