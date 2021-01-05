/*
Description: Quick sort with partition into 3 parts to speed up when there are multiple duplicate elements in array.
*/
#include <iostream>
#include <vector>
#include <cstdlib>

using std::vector;
using std::swap;

int partition2(vector<int>& a, int l, int r) {
    int x = a[l];
    int j = l;
    for (int i = l + 1; i <= r; i++) {
        if (a[i] <= x) {
            j++;
            swap(a[i], a[j]);
        }
    }
    swap(a[l], a[j]);
    return j;
}

vector<int> partition3(vector<int>& a, int l, int r) {
    vector<int> otpt(2);
    int x = a[l];  // pivot
    int less = l;  // less items in [l,less-1]
    int more = r;  // greater items in [more+1,r]
    int i = l;
    
    while (i <= more) {
        if (a[i] < x) {
            swap(a[i], a[less]);
            i++;
            less++;
        }
        else if (a[i] == x) {
            i++;
        }
        else {
            swap(a[i], a[more]);
            more--;
        }
    }
    
    otpt[0] = less; otpt[1] = more;
    return otpt;
}

void randomized_quick_sort(vector<int>& a, int l, int r) {
    if (l >= r) {
        return;
    }
    
    vector<int> otpt = partition3(a, l, r);

    randomized_quick_sort(a, l, otpt[0]-1);
    randomized_quick_sort(a, otpt[1]+1, r);
}

int main() {
    int n;
    std::cin >> n;
    vector<int> a(n);
    for (size_t i = 0; i < a.size(); ++i) {
        std::cin >> a[i];
    }
  
    randomized_quick_sort(a, 0, a.size() - 1);
    for (size_t i = 0; i < a.size(); ++i) {
        std::cout << a[i] << ' ';
    }
}
