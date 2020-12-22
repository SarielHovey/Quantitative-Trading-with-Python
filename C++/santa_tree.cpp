#include <iostream>
#include <windows.h>

using std::cout;
using std::cin;

int CatchInt() {
    int otpt = 0;
    while (true)
    {
        cout << "Input Tree_Height(>=4): ";
        cin >> otpt;
        if (cin.fail()) {
            cin.clear();
            cin.ignore(65525,'\n');
            cout << "Please input an integer!" << "\n";
            continue;  // exit and enter another loop
        }
        else if (otpt <= 3){
            cin.sync();
            cout << "Please input an integer > 3!" << "\n";
            continue;
        }
        else {
            return otpt;
        }
    }
}

void GenerateHead(const int& n) {
    HANDLE hConsole = GetStdHandle(STD_OUTPUT_HANDLE);
    int green=2, red=4;
    int max = 2*n+1;
    for (int i=1; i!=max; i+=2) {
        for (int j=0; j<(n-1-i/2); j++) {
            cout << " ";
        }
        for (int k=0; k!=i; k++) {
            if (k%3 == 0) {
                SetConsoleTextAttribute(hConsole, red);
                cout << "F";
            }
            else {
                SetConsoleTextAttribute(hConsole, green);
                cout << "F";
            }
        }
        cout << "\n";
    }
}

void GenerateRoot(const int& n) {
    HANDLE hConsole = GetStdHandle(STD_OUTPUT_HANDLE);
    int root = 8;
    int max = 2*n+1;
    int n_r = n * 4 / 5; // n_r=0 when n=4 if n/5*4 to avoid overflow
    //cout << "n_r = " << n_r << "\n";
    SetConsoleTextAttribute(hConsole, root);
    for (int i=1; i!=n_r+1; i+=1) {
        for (int j=0; j!=n-3; j++) {
            cout << " ";
        }
        for (int k=0; k!=5; k++) {
            cout << "U";
        }
        cout << "\n";
    }
}

int main() {
    int n = CatchInt();  // get tree_height
    cout << "Merry Christmas!" << "\n";
    GenerateHead(n);
    GenerateRoot(n);
    HANDLE hConsole = GetStdHandle(STD_OUTPUT_HANDLE);
    SetConsoleTextAttribute(hConsole, 6);
    return 0;
}
