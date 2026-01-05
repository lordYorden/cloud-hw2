package hello;

import java.util.regex.Pattern;

public class Utils {

    private static final String EMAIL_REGEX = "^[A-Za-z0-9+_.-]+@(.+)$";

    static boolean IsEmail(String email) {
        return Pattern.matches(EMAIL_REGEX, email);
    }
}
