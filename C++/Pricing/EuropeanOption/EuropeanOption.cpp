#include <iostream>
#include <string>
#include "EuropeanOption.hpp"
#include <math.h>
#define pi 3.141592654

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
    
}
