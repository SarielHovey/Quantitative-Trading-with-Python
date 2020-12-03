#include <iostream>
#include <set>

long long lcm_naive(int a, int b) {
  for (long l = 1; l <= (long long) a * b; ++l)
    if (l % a == 0 && l % b == 0)
      return l;

  return (long long) a * b;
}

long long gcd_fast(int a, int b) {
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
    
long long lcm_fast(int a, int b) {
    long long gcd = gcd_fast(a, b);
    return a / gcd * b;  //avoid overflow as much as possible
}    

int main() {
  int a, b;
  std::cin >> a >> b;
  //std::cout << lcm_naive(a, b) << std::endl;
  std::cout << lcm_fast(a, b) << std::endl;
  return 0;
}
