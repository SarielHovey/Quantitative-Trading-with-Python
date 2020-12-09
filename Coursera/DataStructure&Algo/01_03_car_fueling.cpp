#include <iostream>
#include <list>

using std::cin;
using std::cout;
using std::list;

int least_left_close (int location, int dist) {
    
}


int compute_min_refills(int dist, int tank, list<double> & stops) {
    int n = 0;
    double diff = 0.0;
    double last_fill = 0.0;
    list<double>::iterator itr;
    while (stops.size() != 1) {
        diff = *std::next(stops.begin()) - *(stops.begin());
        if (diff > 1.0) {
            return -1;
        }
        else {
            stops.pop_front();
            diff = *std::next(stops.begin()) - *(stops.begin());
            if (*std::next(stops.begin()) > (last_fill+1)) {
                n++;
                last_fill = *stops.begin();
                stops.pop_front();
                cout << "pop with n+1" << "\n";
            }
            else {
                stops.pop_front();
                cout << "pop with n unchanged!" << "\n";
            }
        }
    }
    return n;
}

int main() {
    int dist = 0;
    cin >> dist;
    int tank = 0;
    cin >> tank;
    int n = 0;
    cin >> n;
    int tmp = 0;

    list<double> stops;
    for (size_t i = 0; i != n; ++i) {
        cin >> tmp;
        stops.push_back(tmp / tank);
    }
    stops.push_front(0.0);
    stops.push_back(dist / tank);
 
    cout << compute_min_refills(dist, tank, stops) << "\n";

    return 0;
}
