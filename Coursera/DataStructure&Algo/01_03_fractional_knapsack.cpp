#include <iostream>
#include <vector>
#include <algorithm>

using std::vector;

struct item {
    int weight = 0;
    int value = 0;
    double rank = 0.0; // wight / value
    bool operator< (const item& another) {
        return this->rank < another.rank;
    }
};


double get_optimal_value(const int& capacity, const vector<item>& items) {
    double value = 0.0;
    int load = 0;
    vector<item>::const_reverse_iterator itr;

    std::sort(items.begin(),items.end());
    for ( itr=items.crbegin(); itr!=items.crend(); itr++) {
        if (((*itr).weight + load) < capacity) {
            load += (*itr).weight;
            value += (*itr).value;
        }
        else if (((*itr).weight + load) == capacity) {
            return (value + (*itr).value);
        }
        else {
            int weight_gap = capacity - load;
            double value_part = weight_gap / ((*itr).weight) * ((*itr).value);
            value += value_part;
        }
    }
    
    return value;
}

int main() {
  int n;
  int capacity;
  std::cin >> n >> capacity;
  vector<item> items(n);
  for (int i = 0; i != n; i++) {
    std::cin >> items[i].value >> items[i].weight;
    items[i].rank = items[i].value / items[i].weight;
  }

  double optimal_value = get_optimal_value(capacity, items);

  std::cout.precision(10);
  std::cout << optimal_value << std::endl;
  return 0;
}
