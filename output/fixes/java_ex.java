public class Calculator {
    // Methods renamed for better clarity and correctness

    public int add(int a, int b) { // Adds two integers
        return a + b;
    }

    public int subtract(int a, int b) { // Subtracts second integer from first
        return a - b;
    }

    public int multiply(int a, int b) { // Multiplies two integers
        int result = a * b; // Perform multiplication
        return result; // Return the result of multiplication
    }

    public double divide(int a, int b) { // Divides first integer by second
        if (b == 0) { // Check for division by zero
            throw new ArithmeticException("Division by zero"); // Throw exception for division by zero
        }
        return (double) a / b; // Cast to double before returning
    }

    public int factorial(int n) { // Computes factorial of a non-negative integer
        if (n < 0) { // Check for negative input
            throw new IllegalArgumentException("Factorial not defined for negative numbers"); // Throw exception for negative input
        }
        if (n == 0 || n == 1) {
            return 1; // Base case: 0! and 1! are both 1
        }
        int result = 1; // Initialize result to 1
        for (int i = 2; i <= n; i++) { // Loop from 2 to n inclusive
            result *= i; // Multiply result by i
        }
        return result; // Return the computed factorial
    }
}