#ifndef __VANILLA_OPTION_CPP
#define __VANILLA_OPTION_CPP
#endif
#include "vanilla_option.hpp"
#include <cmath>
/* For test
#include <iostream>
using namespace std;
*/

double N(const double& value) {
    return 0.5 * erfc(-value * sqrt(0.5));
};

void VanillaOption::init() {
    K = 100.0;
    r = 0.05;
    T = 1.0;
    S = 100.0;
    sigma = 0.2;
};

void VanillaOption::copy(const VanillaOption& rhs) {
    //pass by reference to const
    K = rhs.getK();
    r = rhs.getr();
    T = rhs.getT();
    S = rhs.getS();
    sigma = rhs.getsigma();
};

VanillaOption::VanillaOption() {
    init();
};

VanillaOption::VanillaOption(const double& _K, const double& _r,
            const double& _T, const double& _S,
            const double& _sigma) {
    K = _K;
    r = _r;
    T = _T;
    S = _S;
    sigma = _sigma;
};

VanillaOption::VanillaOption(const VanillaOption& rhs) {
    copy(rhs);
};

VanillaOption& VanillaOption::operator = (const VanillaOption& rhs) {
    //allow Chain assignment
    if (this == &rhs) return *this;
    copy(rhs);
    return *this;
};

VanillaOption::~VanillaOption() {};

double VanillaOption::getK() const { return K;};
double VanillaOption::getr() const { return r;};
double VanillaOption::getT() const { return T;};
double VanillaOption::getS() const { return S;};
double VanillaOption::getsigma() const { return sigma;};

double VanillaOption::calc_call_price() const {
    //default 10.45058
    double sigma_sqrt_T = sigma * sqrt(T);
    double d_1 = ( log(S/K) + (r + 0.5*sigma*sigma)*T ) / sigma_sqrt_T;
    double d_2 = d_1 - sigma_sqrt_T;
    return S*N(d_1) - K*exp(-r*T)*N(d_2);
}

double VanillaOption::calc_put_price() const {
    //default 5.573526
    double sigma_sqrt_T = sigma * sqrt(T);
    double d_1 = ( log(S/K) + (r + 0.5*sigma*sigma)*T ) / sigma_sqrt_T;
    double d_2 = d_1 - sigma_sqrt_T;
    return -S*N(-d_1) + K*exp(-r*T)*N(-d_2);
};

/* For Test
int main() {
    VanillaOption Op1;
    cout << Op1.calc_call_price() << endl;
    cout << Op1.calc_put_price() << endl;
    return 0;
}
*/