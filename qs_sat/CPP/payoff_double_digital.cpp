#include "payoff.hpp"

PayOffDoubleDigital::PayOffDoubleDigital(const double& U_, const double& D_)
{
U = U_;
D = D_;
};

PayOffDoubleDigital::~PayOffDoubleDigital() {};

double PayOffDoubleDigital::operator() (const double& S) const {
    if (S >= D && S <= U) {
        return 1.0;
    } else
    {
        return 0.0;
    }   
};