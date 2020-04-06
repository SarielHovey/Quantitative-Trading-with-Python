#include "payoff.hpp"

PayOffPut::PayOffPut(const double& K_)
{
K = K_;
};

PayOffPut::~PayOffPut() {};

double PayOffPut::operator() (const double& S) const {
    return std::max(K-S, 0.0);
};