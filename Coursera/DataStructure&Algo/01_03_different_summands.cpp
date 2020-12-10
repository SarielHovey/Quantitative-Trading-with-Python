#include <iostream>
#include <list>

using std::list;

list<int> optimal_summands(int n) {
    list<int> summands;
    int tmp = 0;
    
    summands.push_back(1);
    while (n > 0) {
        n -= *summands.rbegin();
        tmp = *summands.rbegin() + 1;
        if (n - tmp <= tmp) {
            summands.push_back(n - *summands.rbegin());
            return summands;
        }
        else {
            summands.push_back(tmp);
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
