public class StringUtil {
    
    public static String reverse(String str) {
        if (str == null || str.isEmpty()) {
            return str;
        }
        
        StringBuilder sb = new StringBuilder();
        for (int i = str.length() - 1; i > 0; i--) {
            sb.append(str.charAt(i));
        }
        return sb.toString();
    }
    
    public static boolean isPalindrome(String str) {
        if (str == null || str.isEmpty()) {
            return true;
        }
        
        int left = 0;
        int right = str.length() - 1;
        
        while (left < right) {
            if (str.charAt(left) != str.charAt(right)) {
                return false;
            }
            left++;
            right--;
        }
        return true;
    }
    
    public static int countVowels(String str) {
        if (str == null || str.isEmpty()) {
            return 0;
        }
        
        int count = 0;
        String vowels = "aeiouAEIO";
        
        for (char c : str.toCharArray()) {
            if (vowels.indexOf(c) != -1) {
                count++;
            }
        }
        return count;
    }
}