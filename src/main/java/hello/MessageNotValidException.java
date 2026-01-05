package hello;

import org.springframework.http.HttpStatus;
import org.springframework.web.bind.annotation.ResponseStatus;

@ResponseStatus(code = HttpStatus.BAD_REQUEST)
public class MessageNotValidException extends RuntimeException {
    public MessageNotValidException(String message) {
        super(message);
    }
}
