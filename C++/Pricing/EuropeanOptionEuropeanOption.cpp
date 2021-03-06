#include <iostream>
#include "EuropeanOption.hpp"
#include <cmath>
#define pi 3.1415926535897932
using namespace std;
//Realize functions in hpp file
double EuropeanOption::N(double x) const
{
    // constants
    double a1 =  0.254829592;
    double a2 = -0.284496736;
    double a3 =  1.421413741;
    double a4 = -1.453152027;
    double a5 =  1.061405429;
    double p  =  0.3275911;

    // Save the sign of x
    int sign = 1;
    if (x < 0)
        sign = -1;
    x = fabs(x)/sqrt(2.0);

    // A&S formula 7.1.26
    double t = 1.0/(1.0 + p*x);
    double y = 1.0 - (((((a5*t + a4)*t) + a3)*t + a2)*t + a1)*t*exp(-x*x);

    return 0.5*(1.0 + sign*y);
}

double EuropeanOption::CallPrice() const
{
    double tmp = sigma * sqrt(T);
    double d1 = ( log(S0/K) + (r - q + sigma*sigma*0.5)*T) / tmp;
    double d2 = d1 - tmp;
    return (S0 * exp((-q)*T)*N(d1)) - (K*exp(-r*T)*N(d2));
}

double EuropeanOption::PutPrice() const
{
    double tmp = sigma * sqrt(T);
    double d1 = (log(S0/K) + (r - q + sigma*sigma*0.5)*T) / tmp;
    double d2 = d1 - tmp;
    return (-S0 * exp((-q)*T)*N(-d1)) + (K*exp(-r*T)*N(-d2));
}

double EuropeanOption::CallDelta() const
{
    double tmp = sigma * sqrt(T);
    double d1 = ( log(S0/K) + (r - q + sigma*sigma*0.5)*T) / tmp;
    return exp(-q*T)*N(d1);
}

double EuropeanOption::PutDelta() const
{
    double tmp = sigma * sqrt(T);
    double d1 = ( log(S0/K) + (r - q + sigma*sigma*0.5)*T) / tmp;
    return -exp(-q*T)*N(-d1);
}

double EuropeanOption::CallGamma() const
{
    double tmp = sigma * sqrt(T);
    double d1 = ( log(S0/K) + (r - q + sigma*sigma*0.5)*T) / tmp;
    return exp(-q*T - 0.5*d1*d1) / (S0*tmp * sqrt(2*pi));
}

double EuropeanOption::PutGamma() const
{
    double tmp = sigma * sqrt(T);
    double d1 = ( log(S0/K) + (r - q + sigma*sigma*0.5)*T) / tmp;
    return exp(-q*T - 0.5*d1*d1) / (S0*tmp * sqrt(2*pi));
}

double EuropeanOption::CallVega() const
{
    double tmp = sigma * sqrt(T);
    double d1 = ( log(S0/K) + (r - q + sigma*sigma*0.5)*T) / tmp;
    return S0 * exp(-q*T-0.5*d1*d1) * T / sqrt(2*pi);
}

double EuropeanOption::PutVega() const
{
    double tmp = sigma * sqrt(T);
    double d1 = ( log(S0/K) + (r - q + sigma*sigma*0.5)*T) / tmp;
    return S0 * exp(-q*T-0.5*d1*d1) * T / sqrt(2*pi);
}

double EuropeanOption::CallTheta() const
{
    double tmp = sigma * sqrt(T);
    double d1 = ( log(S0/K) + (r - q + sigma*sigma*0.5)*T) / tmp;
    double d2 = d1 - tmp;
    double T1 = S0*sigma*exp(-q*T - 0.5*d1*d1) / (2*sqrt(2*pi*T));
    return -T1 + q*(S0 * exp((-q)*T)*N(d1)) - r*(K*exp(-r*T)*N(d2));
}

double EuropeanOption::PutTheta() const
{
    double tmp = sigma * sqrt(T);
    double d1 = ( log(S0/K) + (r - q + sigma*sigma*0.5)*T) / tmp;
    double d2 = d1 - tmp;
    double T1 = S0*sigma*exp(-q*T - 0.5*d1*d1) / (2*sqrt(2*pi*T));
    return -T1 - q*(S0 * exp((-q)*T)*N(-d1)) + r*(K*exp(-r*T)*N(-d2));
}

double EuropeanOption::CallRho() const
{
    double tmp = sigma * sqrt(T);
    double d2 = ( log(S0/K) + (r - q - sigma*sigma*0.5)*T) / tmp;
    return K*T*exp(-r*T)*N(d2);
}

double EuropeanOption::PutRho() const
{
    double tmp = sigma * sqrt(T);
    double d2 = ( log(S0/K) + (r - q - sigma*sigma*0.5)*T) / tmp;
    return -K*T*exp(-r*T)*N(-d2);
}

void EuropeanOption::init()
{
    // Initialize or Reset value
    r = 0.08;
    sigma = 0.30;
    K = 50.00;
    T = 1.00;
    S0 = 50.00;
    q = 0.00;
    optType = 0;
}

void EuropeanOption::copy(const EuropeanOption& o2)
{
    r = o2.r;
    sigma = o2.sigma;
    K = o2.K;
    T = o2.T;
    S0 = o2.S0;
    q = o2.q;
    optType = o2.optType;
}

EuropeanOption::EuropeanOption()
{
    init();
}

EuropeanOption::EuropeanOption(double t_r, double t_sigma, double t_K, double t_T, double t_S0, double t_q, int t_optType)
{
    r = t_r;
    sigma = t_sigma;
    K = t_K;
    T = t_T;
    S0 = t_S0;
    q = t_q;
    optType = t_optType;    
}

EuropeanOption::EuropeanOption(const EuropeanOption& o2)
{
    //Copy Constructer
    copy(o2);
}


EuropeanOption::~EuropeanOption()
{
}

// 此处重载对类的'='运算符,将其等价为 Deep Copy
EuropeanOption& EuropeanOption::operator= (const EuropeanOption& opt2)
{   // deep copy
    if (this == &opt2) return *this;
    copy(opt2);
    return *this;
}

double EuropeanOption::Price() const
{
    if (optType == 0) {return CallPrice();} else {return PutPrice();}
}

double EuropeanOption::Delta() const
{
    if (optType == 0) {return CallDelta();} else {return PutDelta();}    
}

double EuropeanOption::Gamma() const
{
    if (optType == 0) {return CallGamma();} else {return PutGamma();}
}

double EuropeanOption::Theta() const
{
    if (optType == 0) {return CallTheta();} else {return PutTheta();}
}

double EuropeanOption::Vega() const
{
    if (optType == 0) {return CallVega();} else {return PutVega();}
}

double EuropeanOption::Rho() const
{
    if (optType == 0) {return CallRho();} else {return PutRho();}
}

void EuropeanOption::toggle()
{
    //Switch Option Type
    if (optType == 0) {optType = 1;} else {optType = 0;}
}


int main()
{
    EuropeanOption Opt1;
    double x1;
    x1 = Opt1.Price();
    std::cout << x1 << std::endl;
    return 0;
}
