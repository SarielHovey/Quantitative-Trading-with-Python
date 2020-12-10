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
    while (stops.size() != 1) {
        diff = *std::next(stops.begin()) - *(stops.begin());
        if (diff > 1.0) {
            return -1;
        }
        else {
            if (*std::next(stops.begin()) - last_fill > 1.0) {
                //cout << *std::next(stops.begin()) << " - ";
                //cout << last_fill << "\n";
                n++;
                last_fill = *stops.begin();
                stops.pop_front();
                //cout << "pop with n+1" << "\n";
            }
            else {
                //cout << *std::next(stops.begin()) << " - ";
                //cout << last_fill << "\n";
                stops.pop_front();
                //cout << "pop with n unchanged!" << "\n";
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
        stops.push_back((double) tmp / tank);  // int / int = int if not transformed!!!
    }
    stops.push_back((double) dist / tank);
    
    if (*stops.begin() > 1) {
        cout << -1 << "\n";
        return 0;
    }
 
    cout << compute_min_refills(dist, tank, stops) << "\n";

    return 0;
}
