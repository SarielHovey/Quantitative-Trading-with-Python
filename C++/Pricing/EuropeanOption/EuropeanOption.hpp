class EuropeanOption
{
private:
    void init();
    void copy(const EuropeanOption& o2);
    /* Kernel Functions for price and Greeks */
    double CallPrice() const;
    double PutPrice() const;
    double CallDelta() const;
    double PutDelta() const;
    double CallGamma() const;
    double PutGamma() const;
    double CallVega() const;
    double PutVega() const;
    double CallTheta() const;
    double PutTheta() const;
    double CallRho() const;
    double PutRho() const;
    /* data */
public:
    double r;
    double sigma;
    double K;
    double T;
    double S0;
    double q;
    string optType;

public:
EuropeanOption();
EuropeanOption(const EuropeanOption& option2);
EuropeanOption(const string& optionType);

virtual ~EuropeanOption();

EuropeanOption& operator = (const EuropeanOption& option2);
double Price() const;
double Delta() const;
double Gamma() const;
double Vega() const;
double Theta() const;
double Rho() const;

void toggle();

};

