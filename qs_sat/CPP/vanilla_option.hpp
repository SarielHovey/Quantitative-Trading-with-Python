#ifndef __VANILLA_OPTION_H
#define __VANILLA_OPTION_H
#endif

class VanillaOption {
    private:
        void init();
        void copy(const VanillaOption& rhs);

        double K;
        double r;
        double T;
        double S;
        double sigma;

    public:
        VanillaOption(); //Default constructor
        VanillaOption(const double& _K, const double& _r,
            const double& _T, const double& _S,
            const double& _sigma); //Parameter constructor
        VanillaOption(const VanillaOption& rhs); //Copy constructor
        VanillaOption& operator = (const VanillaOption& rhs); //Assignment operator
        virtual ~VanillaOption(); //Virtual Destructor

        //Selector methods
        double getK() const;
        double getr() const;
        double getT() const;
        double getS() const;
        double getsigma() const;

        //Option price calculation methods
        double calc_call_price() const;
        double calc_put_price() const;
};