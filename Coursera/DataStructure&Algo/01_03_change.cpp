#include <iostream>

int get_change(int m) {
    int n10 = (int) m / 10;
    int resid = m % 10;
    int n5 = (int) resid / 5;
    resid = resid % 5;
    int n1 = resid;

    return n1 + n5 + n10;
}

int main() {
  int m;
  std::cin >> m;
  std::cout << get_change(m) << '\n';
}
