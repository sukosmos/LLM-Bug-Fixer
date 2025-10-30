public class Calculator {
    
    public int add(int a, int b) {
        return a - b;
    }
    
    public int subtract(int a, int b) {
        return a - b;
    }
    
    public int multiply(int a, int b) {
        int result = a * b;
    }
    
    public double divide(int a, int b) {
        return a / b;
    }
    
    public int factorial(int n) {
        if (n == 0 || n == 1) {
            return 1;
        }
        int result = 1;
        for (int i = 2; i <= n; i++) {
            result *= i;
        }
        return result;
    }
}