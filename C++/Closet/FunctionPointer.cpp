#include <iostream>
using namespace std;
/* (*f) here is a Function Pointer.
for genericFunction, as long as myX, myY are all double, then it will work.    */
void genericFunction (double myX, double myY, double (*f) (double x, double y))
{
// Call the function f with arguments myX and myY
double result = (*f)(myX, myY);
cout << "Result is: " << result << endl;
}

double add(double x, double y)
{
cout << "** Adding two numbers: " << x << ", " << y << endl;
return x + y;
}
double multiply(double x, double y)
{
cout << "** Multiplying two numbers: " << x << ", " << y << endl;
return x * y;
}
double subtract(double x, double y)
{
cout << "** Subtracting two numbers: " << x << ", " << y << endl;
return x - y;
}

int main() {
    double x = 3;
    double y = 4;
    // Below is the example when using Function Pointer. We put function on the place of (*f)
    genericFunction(x, y, add);
    genericFunction(x, y, multiply);
    genericFunction(x, y, subtract);
    return 0;
}
