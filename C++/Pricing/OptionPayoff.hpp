// An example of Canonical Header File of payoff for options
#include <iostream>
using namespace std;
class Payoff
{
public:
    Payoff();
    Payoff(const Payoff& source);
    virtual ~Payoff();

    Payoff& operator = (const Payoff& source);
    // With virtual payoff(), the class is a basic class that cannot have instances
    virtual double payoff(double S) const = 0;
};

class CallPayoff: public Payoff
{
private:
    double K;
public:
    CallPayoff();
    CallPayoff(const CallPayoff& source);
    ~CallPayoff();

    CallPayoff& operator = (const CallPayoff& source);
    // Must realize the payoff() function in base class Payoff()
    double payoff(double S) const;

};

class PutPayoff: public Payoff
{
private:
    double K;
public:
    PutPayoff();
    PutPayoff(const PutPayoff& source);
    ~PutPayoff();

    PutPayoff& operator = (const PutPayoff& source);

    double payoff(double S) const;
};

class BullCallPf: public Payoff
{
private:
    double K_Cl;    // Strike price for the long call
    double K_Ch;    // Strike price for the short call
public:
    BullCallPf();
    BullCallPf(const BullCallPf& source);
    ~BullCallPf();

    BullCallPf& operator = (const BullCallPf& source);

    double payoff(double S) const;
};

class BearCallPf: public Payoff
{
private:
    double K_Cl;    // Strike price for the short call
    double K_Ch;    // Strike price for the long call
public:
    BearCallPf();
    BearCallPf(const BearCallPf& source);
    ~BearCallPf();

    BearCallPf& operator = (const BearCallPf& source);

    double payoff(double S) const;
};

class BullPutPf: public Payoff
{
private:
    double K_Pl;    // Strike price for the long put
    double K_Ph;    // Strike price for the short put
public:
    BullPutPf();
    BullPutPf(const BullPutPf& source);
    ~BullPutPf();

    BullPutPf& operator = (const BullPutPf& source);

    double payoff(double S) const;
};

class BearPutPf: public Payoff
{
private:
    double K_Pl;    // Strike price for the short put
    double K_Ph;    // Strike price for the long put
public:
    BearPutPf();
    BearPutPf(const BearPutPf& source);
    ~BearPutPf();

    BearPutPf& operator = (const BearPutPf& source);

    double payoff(double S) const;
};

class ButterflyCallPf: public Payoff
{   // Default as Long Call Butterfly
private:
    double K_Cl;    // Strike price for the long call with lowest K
    double K_Ch;    // Strike price for the long call with highest K
    double K_Cm;    // Strike price for the 2 short calls with medium K
public:
    ButterflyCallPf();
    ButterflyCallPf(const ButterflyCallPf& source);
    ~ButterflyCallPf();

    ButterflyCallPf& operator = (const ButterflyCallPf& source);

    double payoff(double S) const;
};

class ButterflyPutPf: public Payoff
{   // Default as Long Put Butterfly
private:
    double K_Pl;    // Strike price for the long put with lowest K
    double K_Ph;    // Strike price for the long put with highest K
    double K_Pm;    // Strike price for the 2 short puts with medium K
public:
    ButterflyPutPf();
    ButterflyPutPf(const ButterflyPutPf& source);
    ~ButterflyPutPf();

    ButterflyPutPf& operator = (const ButterflyPutPf& source);

    double payoff(double S) const;
};

class Straddle: public Payoff
{
private:
    double K_CP;    // Strike price for long call and long put
public:
    Straddle();
    Straddle(const Straddle& source);
    ~Straddle();

    Straddle& operator = (const Straddle& source);

    double payoff(double S) const;
};