/*
Description: Given a number of segments [a,b], check if a set of points provided are within any segment.
    Additionally, points provided is unordered, and output should also be for unordered points.
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

list<pair<int, int> > fast_count_segments(const vector<int>& starts, const vector<int>& ends, const vector<pair<int, int> >& points) {
    list<pair<int, int> > cnt;
    
    size_t total_num = starts.size() + ends.size();
    list< pair<int, int> > line(total_num);
    for (size_t i=0; i != starts.size(); i++) {
        line.push_back({starts[i],1});
    }
    for (size_t j=0; j != ends.size(); j++) {
        line.push_back({ends[j],-1});
    }
    
    line.sort([](const pair<int, int>& a, const pair<int, int>& b) -> bool {
            return a.first < b.first;
        }
    );
    
    int cnt_i = 0;  // must be out of below loop to accumulate count of lower bound
    for (vector<pair<int, int> >::const_iterator itr = points.cbegin(); itr != points.cend(); itr++) {

        while (!line.empty() && line.front().first < (*itr).first) {
            cnt_i += line.front().second;
            line.pop_front();
        }
        cnt.push_back({std::move(cnt_i), (*itr).second});  // match count with order before sort in "points"
    }
    
    return cnt;
}

int main() {
    int n, m; // n - Number of segments on line; m - Number of points on line;
    cin >> n >> m;
    vector<int> starts(n), ends(n); // starts - lower bound of ith segment; ends - upper bound of ith segment;
    for (size_t i = 0; i < starts.size(); i++) {
        cin >> starts[i] >> ends[i];
    }
    vector<pair<int, int> > points(m);  // defining points
    int tmp;
    for (int i=0; i != m; i++) {
        cin >> tmp;
        points[i] = {tmp,i};  // i here stores order before sort
    }
    std::sort(points.begin(), points.end(), [](const pair<int, int>& a, const pair<int, int>& b) -> bool {
            return a.first < b.first;
        }
    );

    list<pair<int, int> > cnt = fast_count_segments(starts, ends, points);
    
    cnt.sort([](const pair<int, int>& a, const pair<int, int>& b) -> bool {
            return a.second < b.second;
        });
    
    for (list<pair<int, int> >::iterator i = cnt.begin(); i != cnt.end(); i++) {
        cout << (*i).first << ' ';
    }
}
