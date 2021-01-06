#include <iostream>
#include <vector>

using std::cin;
using std::cout;
using std::vector;

void merge(vector<int>& A, int l, int m, int r) {
    int n1 = m - l + 1;
    int n2 = r - m;
    
    vector<int> L(n1), R(n2);
    for (int i = 0; i < n1; i++) {
        L[i] = A[l+i];
    }
    for (int j = 0; j < n2; j++) {
        R[j] = A[m+1+j];
    }
    
    int i = 0, j=0, k=l;
    
    while (i < n1 && j < n2) {
        if (L[i] <= R[j]) {
            A[k] = L[i];
            i++;
            k++;
        }
        else {
            A[k] = R[j];
            j++;
            k++;
        }
    }
    // in case elements left in L or R
    while (i < n1) {
        A[k] = L[i];
        i++; k++;
    }
    
    while (j < n2) {
        A[k] = R[j];
        j++; k++;
    }
    
}

void merge_sort(vector<int>& A, int l, int r) {
    if (l >= r) {
        return;
    }
    
    int m = (l+r-1) / 2;
    merge_sort(A, l, m);
    merge_sort(A, m+1, r);
    merge(A, l, m, r);
}


int main() {
    int n;
    std::cin >> n;
    vector<int> A(n);
    vector<int>::iterator itr;
    for (itr = A.begin(); itr != A.end(); itr++) {
        cin >> *itr;
    }
    merge_sort(A, 0, n-1);
    
    for (itr = A.begin(); itr != A.end(); itr++) {
        cout << *itr << " ";
    }
    
    cout << "\n";
    return 0;
}
