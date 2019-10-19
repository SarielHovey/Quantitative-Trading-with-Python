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


/*
Showing that * and & are inverses of each other.
a= 7
&a= 0x7ffff425062c
*a is not valid as a is an int not pointer.
aPtr= 0x7ffff425062c
&aPtr= 0x7ffff4250630
*aPtr= 7
&*a is not valid as a is an int not pointer.
*&a= 7
&*aPtr = 0x7ffff425062c
*&aPtr = 0x7ffff425062c
&*&a= 0x7ffff425062c
*&*aPtr= 7
&*&aPtr= 0x7ffff4250630
Conclusion:
(1)&a = aPtr, is the Memory Position of a
(2)a = *aPtr, is the value Memory Position of a points to
(3)&*aPtr = *&aPtr = aPtr = &*&a, because & and * are inverses
(4)&aPtr is the Memory Position of aPtr, which points to &a    
*/
