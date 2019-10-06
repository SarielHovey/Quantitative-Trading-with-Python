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
    optType = 1;
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

EuropeanOption::EuropeanOption(double r0, double sigma0, double K0, double T0, double S00, double q0, int optType0)
{
    r = r0;
    sigma = sigma0;
    K = K0;
    T = T0;
    S0 = S00;
    q = q0;
    optType = optType0;
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
    if (optType == 1) {return CallPrice();} else {return PutPrice();}
}

double EuropeanOption::Delta() const
{
    if (optType == 1) {return CallDelta();} else {return PutDelta();}    
}

double EuropeanOption::Gamma() const
{
    if (optType == 1) {return CallGamma();} else {return PutGamma();}
}

double EuropeanOption::Theta() const
{
    if (optType == 1) {return CallTheta();} else {return PutTheta();}
}

double EuropeanOption::Vega() const
{
    if (optType == 1) {return CallVega();} else {return PutVega();}
}

double EuropeanOption::Rho() const
{
    if (optType == 1) {return CallRho();} else {return PutRho();}
}

void EuropeanOption::toggle()
{
    //Switch Option Type
    if (optType == 1) {optType = 1;} else {optType = 0;}
}


int main()
{
    EuropeanOption Opt1(0.1,0.3,50,0.5,50,0.00,1);
    cout << "Opt Type: " << Opt1.optType << endl;
    cout << "Price: " << Opt1.Price() << endl;
    cout << "Delta: " << Opt1.Delta() << endl;
    cout << "Gamma: " << Opt1.Gamma() << endl;
    cout << "Theta: " << Opt1.Theta() << endl;
    cout << "Rho: " << Opt1.Rho() << endl;
    cout << "Vega: " << Opt1.Vega() << endl;
    return 0;
}