import org.junit.Test;
import static org.junit.Assert.*;

public class StringUtilTest {
    
    @Test
    public void testReverse() {
        assertEquals("Reverse of 'hello' should be 'olleh'", 
                     "olleh", StringUtil.reverse("hello"));
        assertEquals("Reverse of single char", 
                     "a", StringUtil.reverse("a"));
        assertEquals("Reverse of empty string", 
                     "", StringUtil.reverse(""));
        assertNull("Reverse of null should be null", 
                   StringUtil.reverse(null));
    }
    
    @Test
    public void testIsPalindrome() {
        assertTrue("'racecar' is a palindrome", 
                   StringUtil.isPalindrome("racecar"));
        assertTrue("'A' is a palindrome", 
                   StringUtil.isPalindrome("A"));
        assertFalse("'hello' is not a palindrome", 
                    StringUtil.isPalindrome("hello"));
        assertTrue("'Racecar' should be palindrome (case insensitive)", 
                   StringUtil.isPalindrome("Racecar"));
    }
    
    @Test
    public void testCountVowels() {
        assertEquals("'hello' has 2 vowels", 
                     2, StringUtil.countVowels("hello"));
        assertEquals("'AEIOU' has 5 vowels", 
                     5, StringUtil.countVowels("AEIOU"));
        assertEquals("'xyz' has 0 vowels", 
                     0, StringUtil.countVowels("xyz"));
        assertEquals("'Education' has 5 vowels", 
                     5, StringUtil.countVowels("Education"));
    }
}