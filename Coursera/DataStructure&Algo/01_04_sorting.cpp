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
    int x = a[l];
    int less = l;
    int more = r;
    int i = l+1;
    int j = r;
    while (i < j) {
        if (a[i] < x) {
            less++;
            swap(a[i], a[less]);
            i++;
        }
        else if (a[i] == x) {
            i++;
        }
        else {
            i++;
        }
        if (a[j] > x) {
            swap(a[j], a[more]);
            j--;
            more--;          
        }
        else if (a[j] == x) {
            j--;
        }
        else {
            j--;
        }
    }
    swap(a[l], a[less]);
    otpt[0] = less; otpt[1] = more;
    return otpt;
}

void randomized_quick_sort(vector<int>& a, int l, int r) {
    if (l >= r) {
        return;
    }
    
    vector<int> otpt = partition3(a, l, r);

    randomized_quick_sort(a, l, otpt[0]);
    randomized_quick_sort(a, otpt[1], r);
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
