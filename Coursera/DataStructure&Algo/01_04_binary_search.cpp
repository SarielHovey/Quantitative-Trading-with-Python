#include <iostream>
#include <cassert>
#include <algorithm>
#include <vector>

using std::vector;

template <typename Iter, typename T>
Iter binary_find(Iter begin, Iter end, T val)
{
    // Finds the lower bound in at most log(last - first) + 1 comparisons
    Iter itr = std::lower_bound(begin, end, val);

    // lower_bound use < to find items, so dont use (*i == val) here
    // *itr here may be a int larger than or equal to val
    // in below, if val < *itr then val is not found
    if (itr != end && !(val < *itr)) 
        return itr; // found
    else
        return end; // not found
}

int binary_search(vector<int>& a, const int& x) {
    int left = 0, right = (int)a.size();
    
    std::sort(a.begin(), a.end());  // O(nlog n)
    
    vector<int>::const_iterator itr;
    itr = binary_find(a.cbegin(), a.cend(), x);  // Complier will induce T from param
    // itr = binary_find<vector<int>::const_iterator, int>(a.cbegin(), a.cend(), x); Explicit specification also allowed
    if (itr != a.cend()) {
        return itr - a.cbegin();
    }
    else {
        return -1;
    }
}    

int linear_search(const vector<int> &a, int x) {
  for (size_t i = 0; i < a.size(); ++i) {
    if (a[i] == x) return i;
  }
  return -1;
}

int main() {
  int n;
  std::cin >> n;
  vector<int> a(n);
  for (size_t i = 0; i < a.size(); i++) {
    std::cin >> a[i];
  }
  int m;
  std::cin >> m;
  vector<int> b(m);
  for (int i = 0; i < m; ++i) {
    std::cin >> b[i];
  }
  for (int i = 0; i < m; ++i) {
    //replace with the call to binary_search when implemented
    //std::cout << linear_search(a, b[i]) << ' ';
    std::cout << binary_search(a, b[i]) << " ";
  }
}
