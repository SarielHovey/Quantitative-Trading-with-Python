#include "payoff.hpp"

PayOffCall::PayOffCall(const double& K_)
{
K = K_;
};

PayOffCall::~PayOffCall() {};

double PayOffCall::operator() (const double& S) const {
    return std::max(S-K,0.0);
};