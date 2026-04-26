#include <iostream>
#include <stdexcept>

// Calculator class with basic arithmetic operations
class Calculator {
public:
    double add(double a, double b) {
        return a + b;
    }

    double subtract(double a, double b) {
        return a - b;
    }

    double multiply(double a, double b) {
        return a * b;
    }

    double divide(double a, double b) {
        if (b == 0) {
            throw std::invalid_argument("Division by zero is not allowed.");
        }
        return a / b;
    }

    double power(double base, int exp) {
        double result = 1.0;
        bool negative = exp < 0;
        int absExp = negative ? -exp : exp;
        for (int i = 0; i < absExp; ++i) {
            result *= base;
        }
        return negative ? 1.0 / result : result;
    }
};

// Factorial function (recursive)
long long factorial(int n) {
    if (n < 0) throw std::invalid_argument("Factorial of negative number");
    if (n == 0 || n == 1) return 1;
    return n * factorial(n - 1);
}

// Check if a number is prime
bool isPrime(int n) {
    if (n < 2) return false;
    for (int i = 2; i * i <= n; ++i) {
        if (n % i == 0) return false;
    }
    return true;
}

int main() {
    Calculator calc;

    std::cout << "Add: " << calc.add(5, 3) << std::endl;
    std::cout << "Subtract: " << calc.subtract(10, 4) << std::endl;
    std::cout << "Multiply: " << calc.multiply(6, 7) << std::endl;
    std::cout << "Divide: " << calc.divide(15, 3) << std::endl;
    std::cout << "Power: " << calc.power(2, 10) << std::endl;
    std::cout << "Factorial(5): " << factorial(5) << std::endl;
    std::cout << "isPrime(17): " << (isPrime(17) ? "Yes" : "No") << std::endl;

    return 0;
}
