#include <iostream>
#include <vector>
#include <algorithm>

using std::vector;

struct item {
    int weight = 0;
    int value = 0;
    double rank = 0.0; // wight / value
    
    item(int w, int v) {
        weight = w;
        value = v;
        rank = v / w;
    }
    bool operator< (item& another) {
        return this->rank < another.rank;
    }
};

double get_optimal_value(const int capacity, const vector<item>& items) {
    double value = 0.0;
    int load = 0;
    vector<item>::const_reverse_iterator itr;

    for ( itr=items.crbegin(); itr!=items.crend(); itr++) {
        if (((*itr).weight + load) < capacity) {
            load += (*itr).weight;
            value += (*itr).value;
        }
        else {
            double weight_gap = capacity - load;
            double value_part = weight_gap / ((*itr).weight) * ((*itr).value);
            value += value_part;
            std::cout << "In else block" << "\n";
            return value;
        }
    }
}

int main() {
  int n;
  int capacity;
  std::cin >> n >> capacity;
  
  int w=0, v=0;
  vector<item> items;
  
  for (int i = 0; i != n; i++) {
    std::cin >> v >> w;
    items.insert(items.begin(), item(w,v));
  }
  std::sort(items.begin(),items.end()); //sorted in rank
  
  double optimal_value = get_optimal_value(capacity, items);

  std::cout.precision(10);
  std::cout << optimal_value << std::endl;
  return 0;
}
