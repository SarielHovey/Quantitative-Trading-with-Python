/*
Description:
    Given a list of int (e.g. 114,514,810,893,24,1919,3), return the largest int while combining them.
*/

#include <algorithm>
#include <sstream>
#include <iostream>
#include <list>
#include <string>

using std::list;
using std::string;
using std::stringstream;
using std::stoi;

inline bool leq(const int& x1, const int& x2) {
    stringstream s1, s2;
    
    s1 << x1 << x2;
    s2 << x2 << x1;
    
    
    return stoi(s1.str()) < stoi(s2.str());
}

string largest_number(list<int>& a) {
    
    a.sort(leq);  // O(nlogn)
  
    stringstream ret;
    for (list<int>::const_reverse_iterator itr = a.crbegin(); itr != a.crend(); itr++) {
        ret << *itr;    
    }
  
    string result;
    ret >> result;
    return result;
}

int main() {
    int n;
    std::cin >> n;
    list<int> a;
  
    int tmp;
    for (int i=0; i!=n; i++) {
        std::cin >> tmp;
        a.push_back(tmp);
    }
    std::cout << largest_number(a);
}
