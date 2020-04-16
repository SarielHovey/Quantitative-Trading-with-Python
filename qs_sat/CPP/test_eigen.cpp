#include <iostream>
#include <Eigen/Dense> // g++ -I Z:/eigen-3.3.7/ test_eigen.cpp -o test_eigen.exe

int main() {
    // Define 2 matrices, both 3x3
    Eigen::MatrixXd p(3,3);
    Eigen::MatrixXd q(3,3);

    // Define 2 3D vectors
    Eigen::Vector3d r(1,2,3);
    Eigen::Vector3d s(4,5,6);

    p << 1,2,3,
         4,5,6,
         7,8,9;
    q << 10,11,12,
         13,14,15,
         16,17,18;

    std::cout << "r+s=\n" << r+s << std::endl;
    std::cout << "r-s=\n" << r-s << std::endl;
    std::cout << "p+q=\n" << p+q << std::endl;
    std::cout << "p*q=\n" << p*q << std::endl;
    std::cout << "p*r=\n" << p*r << std::endl;
    std::cout << "p*3.14159=\n" << p*3.14159 << std::endl;

    Eigen::MatrixXd t(3,2);
    t = Eigen::MatrixXd::Random(3,2);
    std::cout << "t=\n" << t << std::endl;
    std::cout << "t^T=\n" << t.transpose() << std::endl;
    std::cout << "t=\n" << t << std::endl;
    t.transposeInPlace();
    std::cout << "transposeInPlace\n" << std::endl;
    std::cout << "t=\n" << t << std::endl;
    std::cout << "t^T=\n" << t.transpose() << std::endl;

    std::cout << "r.s=\n" << r.dot(s) << std::endl;
    std::cout << "rxs=\n" << r.cross(s) << std::endl;
}