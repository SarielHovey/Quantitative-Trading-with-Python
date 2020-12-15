/*
Descirption: Find an element that duplicates > 1/2 proporation of the container.
*/
#include <algorithm>
#include <iostream>
#include <vector>
#include <unordered_map>
#include <utility> 

using std::vector;
using std::unordered_multimap;  // unordered set could be used instead
using std::make_pair;

bool get_majority_element(vector<int>& a, int left, int right) {
    if (left == right) return 0;
    
    unordered_multimap<int, int> m;
    float a_size = (float) a.size() / 2;
    vector<int>::iterator itr;
    // below insertion may modify a with std::move
    for (itr = a.begin(); itr != a.end(); itr++) {
        m.insert(make_pair<int, int>(std::move(*itr), 1));
    }
    
    unordered_multimap<int, int>::iterator it;
    int num=0;
    for(it = m.begin(); it != m.end(); it++) {
        num = m.count(it->first);
        // std::cout << "key= " << it->first << ", ";
        // std::cout << "num= " << num << ", ";
        // std::cout << "a_size= " << a_size << "\n";
        if ((float) num > a_size) {
            return 1;
        }
    }
    return 0;
}

int main() {
    int n;
    std::cin >> n;
    vector<int> a(n);
    for (size_t i = 0; i < a.size(); ++i) {
        std::cin >> a[i];
    }
    std::cout << get_majority_element(a, 0, a.size()) << '\n';
}
