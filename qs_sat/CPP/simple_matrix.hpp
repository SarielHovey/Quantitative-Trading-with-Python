#ifndef __SIMPLE_MATRIX_H
#define __SIMPLE_MATRIX_H
#include "simple_matrix.cpp" // Required as a generic Class
#include <vector>


// template is an abstract of classes, like class is an abstract of instances
template <typename Type = double> class SimpleMatrix
{
private:
    std::vector<std::vector<Type> > mat;
public:
    SimpleMatrix();
    SimpleMatrix(const int& rows, const int& cols, const Type& val);
    SimpleMatrix(const SimpleMatrix<Type>& _rhs);
    
    SimpleMatrix<Type>& operator= (const SimpleMatrix<Type>& _rhs);
    
    virtual ~SimpleMatrix();

    // Access to Matrix Data directly, via row and column indices
    std::vector<std::vector<Type> > get_mat() const;
    Type& value(const int& row, const int& col);
};

#endif