/*
Description: Calculate inversions with merge sort algorithm
*/
#include <iostream>
#include <vector>

using std::vector;
using std::cin;
using std::cout;

long long merge(vector<int>& a,long long& num, size_t l, size_t m, size_t r) { 
    size_t i=0, j=0, k=l;
    size_t n1 = m-l+1;
    size_t n2 = r-m;
    vector<int> L(n1), R(n2);
    for (int i = 0; i < n1; i++) {
        L[i] = a[l+i];
    }
    for (int j = 0; j < n2; j++) {
        R[j] = a[m+1+j];
    }
    
    while (i < n1 && j < n2) {
        if (L[i] <= R[j]) {
            a[k] = L[i];
            i++;
            k++;
        }
        else {
            a[k] = R[j];
            num += (n1-i);
            j++;
            k++;
        }
    }
    
    while (i < n1) {
        a[k] = L[i];
        i++; k++;
    }
    
    while (j < n2) {
        a[k] = R[j];
        j++; k++;
    }
    
    return num;
}

long long get_number_of_inversions(vector<int>& a, size_t l, size_t r) {
    long long number_of_inversions = 0;
    if (l >= r) {
        return number_of_inversions;
    }
    size_t m = (l + r) / 2;
    
    number_of_inversions += get_number_of_inversions(a, l, m);
    number_of_inversions += get_number_of_inversions(a, m+1, r);
    number_of_inversions += merge(a, number_of_inversions, l, m, r);
}

int main() {
    int n;
    cin >> n;
    vector<int> a(n);
    for (vector<int>::iterator itr = a.begin(); itr != a.end(); itr++) {
        cin >> *itr;
    }
    // vector<int> b(a.cbegin(), a.cend());
    
    cout << get_number_of_inversions(a, 0, n-1) << '\n';
    
    /* debug only
    for (vector<int>::iterator itr = a.begin(); itr != a.end(); itr++) {
        cout << *itr << " ";
    }
    */
    return 0;
}
