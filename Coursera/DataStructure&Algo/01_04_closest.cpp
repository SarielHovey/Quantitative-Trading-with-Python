/*
Description: Calculate the min distance between a set of points with (x,y) coordinate.
*/

#include <vector>
#include <cmath>
#include <algorithm>
#include <iostream>

using std::vector;
using std::sort;
using std::cin;
using std::cout;
using std::sqrt;

struct Point {
    int x=0, y=0;
};

double _brute_min(vector<Point>& X, size_t n) {
    float min = sqrt((X[0].x-X[1].x)*(X[0].x-X[1].x) + (X[0].y-X[1].y)*(X[0].y-X[1].y));
    float temp = 0.0;
    for (int i=0; i !=n; i++) {
        for (int j=i+1; j!=n; j++) {
            temp = sqrt((X[i].x-X[j].x)*(X[i].x-X[j].x) + (X[i].y-X[j].y)*(X[i].y-X[j].y));
            if (temp < min) {
                min = temp;
            }
        }
    }
    
    return min;
}

double _recursive_min(vector<Point>& X, vector<Point>& Y, size_t n) {
    
    if (n <= 3) {
        return _brute_min(Px, n);
    }
    
    size_t m = n / 2;
    Point mid_point = X[m];
    
    
}

double minimal_distance(vector<Point>& points) {
    double otpt = 0.0;
    vector<Point> Px(points);
    vector<Point> Py(points);
    
    // sort Px on x and Py on y ASC;
    sort(Px.begin(), Px.end(), [](Point& a, Point& b) -> bool {
        return a.x < b.x;
        }
    );
    sort(Py.begin(), Py.end(), [](Point& a, Point& b) -> bool {
        return a.y < b.y;
        }
    );
    
    otpt = _recursive_min(Px, Py, points.size());
    
    return otpt;
}

int main() {
    size_t n;
    cin >> n;
    vector<Point> points(n);
    
    for (vector<Point>::iterator itr = points.begin(); itr != points.end(); itr++) {
        cin >> (*itr).x >> (*itr).y;
    }
    cout.precision(9);
    cout << std::fixed;
    cout << minimal_distance(points) << "\n";
  
    return 0;
}
