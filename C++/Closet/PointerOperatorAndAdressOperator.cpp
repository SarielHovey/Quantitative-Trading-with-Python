#include<iostream>
using namespace std;

int main()
{
    int a;  //a is an integer
    int *aPtr;  //aPtr is a pointer to an integer

    a=7;
    aPtr = &a;
    cout<<"Showing that * and & are inverses of "<<"each other.\n";
    cout<<"a= "<<a<<endl;
    cout<<"&a= "<<&a<<endl;
    cout<<"*a is not valid as a is an int not pointer."<<endl;
    cout<<"aPtr= "<<aPtr<<endl;
    cout<<"&aPtr= "<<&aPtr<<endl;
    cout<<"*aPtr= "<<*aPtr<<endl;
    cout<<"&*a is not valid as a is an int not pointer."<<endl;
    cout<<"*&a= "<<*&a<<endl;
    cout<<"&*aPtr = "<<&*aPtr<<endl;
    cout<<"*&aPtr = "<<*&aPtr <<endl;
    cout<<"&*&a= "<<&*&a<<endl;
    cout<<"*&*aPtr= "<<*&*aPtr<<endl;
    cout<<"&*&aPtr= "<<&*&aPtr<<endl;
    cout<<"Conclusion:\n";
    cout<<"(1)&a = aPtr, is the Memory Position of a"<<endl;
    cout<<"(2)a = *aPtr, is the value Memory Position of a points to"<<endl;
    cout<<"(3)&*aPtr = *&aPtr = aPtr = &*&a, because & and * are inverses"<<endl;
    cout<<"(4)&aPtr is the Memory Position of aPtr, which points to &a"<<endl;
    return 0;
}

