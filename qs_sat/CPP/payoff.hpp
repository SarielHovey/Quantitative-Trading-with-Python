#ifndef PAY_OFF_H
#define PAY_OFF_H
#endif

#include <algorithm>

class PayOff
{
public:
    PayOff() {};
    virtual ~PayOff();

    // Overloaded operator(), turns the PayOff into an abstract function object
    virtual double operator() (const double& S) const =0; // Pure virtual method
};

class PayOffCall : public PayOff
{
private:
    double K;
public:
    PayOffCall(const double& K_) {};
    virtual ~PayOffCall() {};
    virtual double operator() (const double& S) const;
};

class PayOffPut : public PayOff
{
private:
    double K;
public:
    PayOffPut(const double& K_) {};
    virtual ~PayOffPut() {};
    virtual double operator() (const double& S) const;
};

class PayOffDoubleDigital : public PayOff
{
private:
    double U; // Upper strike price
    double D;
public:
    PayOffDoubleDigital(const double& U_, const double& D_);
    virtual ~PayOffDoubleDigital();
    virtual double operator() (const double& S) const;
};