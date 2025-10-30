import org.junit.Test;
import static org.junit.Assert.*;

public class CalculatorTest {
    
    private Calculator calculator = new Calculator();
    
    @Test
    public void testAdd() {
        assertEquals(5, calculator.add(2, 3));
        assertEquals(-1, calculator.add(-3, 2));
        assertEquals(5, calculator.add(5, 0));
    }
    
    @Test
    public void testSubtract() {
        assertEquals(2, calculator.subtract(5, 3));
        assertEquals(-5, calculator.subtract(0, 5));
    }
    
    @Test
    public void testMultiply() {
        assertEquals(6, calculator.multiply(2, 3));
        assertEquals(0, calculator.multiply(5, 0));
        assertEquals(-10, calculator.multiply(-5, 2));
    }
    
    @Test
    public void testDivide() {
        assertEquals(2.0, calculator.divide(6, 3), 0.001);
        assertEquals(2.5, calculator.divide(5, 2), 0.001);
    }
    
    @Test(expected = ArithmeticException.class)
    public void testDivideByZero() {
        calculator.divide(5, 0);
    }
    
    @Test
    public void testFactorial() {
        assertEquals(1, calculator.factorial(0));
        assertEquals(1, calculator.factorial(1));
        assertEquals(120, calculator.factorial(5));
    }
    
    @Test(expected = IllegalArgumentException.class)
    public void testFactorialNegative() {
        calculator.factorial(-5);
    }
}