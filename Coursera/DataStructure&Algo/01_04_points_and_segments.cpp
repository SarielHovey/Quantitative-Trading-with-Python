/*
Description: Given a number of segments [a,b], check if a set of points provided are within any segment.
*/
#include <iostream>
#include <vector>
#include <list>
#include <utility>
#include <functional>   // std::greater
#include <algorithm>    // std::sort

using std::cout;
using std::cin;
using std::vector;
using std::list;
using std::pair;
using std::make_pair;

vector<int> naive_count_segments(const vector<int>& starts, const vector<int>& ends, const vector<int>& points) {
    vector<int> cnt(points.size());
    for (size_t i = 0; i < points.size(); i++) {
        for (size_t j = 0; j < starts.size(); j++) {
        cnt[i] += (starts[j] <= points[i] && points[i] <= ends[j]);
        }
    }
    return cnt;
}

list<int> fast_count_segments(const vector<int>& starts, const vector<int>& ends, const vector<int>& points) {
    list<int> cnt(points.size());
    
    size_t total_num = starts.size() + ends.size();
    list< pair<int, int> > line(total_num);
    for (size_t i=0; i != starts.size(); i++) {
        line.push_back({starts[i],1});
    }
    for (size_t j=0; j != ends.size(); j++) {
        line.push_back({ends[j]+1,-1});
    }
    
    line.sort([](const pair<int, int>& a, const pair<int, int>& b) -> bool {
            return a.first < b.first;
        }
    );
    
    
    return cnt;
}

int main() {
    int n, m; // n - Number of segments on line; m - Number of points on line;
    cin >> n >> m;
    vector<int> starts(n), ends(n); // starts - lower bound of ith segment; ends - upper bound of ith segment;
    for (size_t i = 0; i < starts.size(); i++) {
        cin >> starts[i] >> ends[i];
    }
    vector<int> points(m);  // defining points
    vector<int>::iterator itr;
    for (itr = points.begin(); itr != points.end(); itr++) {
        cin >> *itr;
    }
    std::sort(points.begin(), points.end());

    list<int> cnt = fast_count_segments(starts, ends, points);
    for (list<int>::iterator i = cnt.begin(); i != cnt.end(); i++) {
        cout << *i << ' ';
    }
}
