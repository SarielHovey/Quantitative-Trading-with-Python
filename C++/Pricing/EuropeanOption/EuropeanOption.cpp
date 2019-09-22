#include <iostream>
#include <string>
#include "EuropeanOption.hpp"
#include <math.h>
#define pi 3.1415926535897932

//Realize functions in hpp file
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
    optType = 'C';
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

EuropeanOption::EuropeanOption(const EuropeanOption& o2)
{
    //Copy Constructer
    copy(o2);
}

EuropeanOption::EuropeanOption(const string& optionType)
{
    optType = optionType;
    if (optType == 'c')
        optType == 'C';
}

EuropeanOption::~EuropeanOption()
{
}

EuropeanOption& EuropeanOption::operator= (const EuropeanOption& opt2)
{   // deep copy
    if (this == &opt2) return *this;
    copy(opt2);
    return *this;
}

