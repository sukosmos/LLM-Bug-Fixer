package com.example;

import java.util.regex.Pattern;
import java.util.regex.Matcher;

public class StringUtil {

    public static String reverse(String str) {
        if (str == null) {
            return null;
        }
        
        StringBuilder sb = new StringBuilder();
        for (int i = str.length() - 1; i >= 0; i--) {
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
        
        while (left <= right) {
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
        
        String vowels = "aeiouAEIOU";
        int count = 0;
        Pattern pattern = Pattern.compile(vowels);
        Matcher matcher = pattern.matcher(str);
        
        while (matcher.find()) {
            count++;
        }
        return count;
    }
}