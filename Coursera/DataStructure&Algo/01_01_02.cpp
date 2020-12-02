#include <iostream>
#include <set>
#include <algorithm>

long long MaxPairwiseProduct(const std::multiset<long long>& numbers) {
    long long max_product = 1;
    std::multiset<long long>::const_reverse_iterator itr= numbers.crbegin();
    
    for (int i=0; i!=2; i++) {
        max_product *= (*itr);
        itr++;
    }

    return max_product;
}

int main() {
    int n;
    std::cin >> n;
    std::multiset<long long> numbers;

    long long tmp;
    for (int i = 0; i < n; ++i) {
        std::cin >> tmp;
        numbers.insert(tmp);
    }
    
    std::cout << MaxPairwiseProduct(numbers) << "\n";
    return 0;
}
