#include <iostream>
#include <list>

using std::list;

list<int> optimal_summands(int n) {
    list<int> summands;
    int tmp = 0;
    
    if (n == 1) {
        summands.push_back(1);
        return summands;
    }
    if (n == 2) {
        summands.push_back(2);
        return summands;
    }
    
    summands.push_back(1);
    while (n > 0) {
        n -= *summands.rbegin(); // n=5
        tmp = *summands.rbegin() + 1; // tmp=3
        if (n - tmp <= tmp) {
            summands.push_back(n);
            return summands;
        }
        else {
            summands.push_back(tmp); // 1,2
        }        
    }
    
    return summands;
}

int main() {
  int n;
  std::cin >> n;
  list<int> summands = optimal_summands(n);
  std::cout << summands.size() << '\n';
  for (list<int>::iterator itr = summands.begin(); itr != summands.end(); itr++) {
    std::cout << *itr << ' ';
  }
}
