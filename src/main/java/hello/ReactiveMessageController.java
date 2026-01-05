package hello;

import org.springframework.http.MediaType;
import org.springframework.web.bind.annotation.*;
import reactor.core.publisher.Flux;
import reactor.core.publisher.Mono;

@RestController
@RequestMapping(
        path = {"/messages"}
)
public class ReactiveMessageController {
    private final ReactiveMessageService service;

    public ReactiveMessageController(ReactiveMessageService service) {
        this.service = service;
    }

    @PostMapping(
            consumes = {MediaType.APPLICATION_JSON_VALUE},
            produces = {MediaType.APPLICATION_JSON_VALUE}
    )
    public Mono<MessageBoundary> create(@RequestBody MessageBoundary input) {
        return service.create(input);
    }

/*    @GetMapping(
            produces = {MediaType.APPLICATION_JSON_VALUE})
    public Mono<MessageBoundary> getById(
            @RequestParam(name = "search") String search,
            @RequestParam(name = "value", required = false, defaultValue = "null") String value) {

        return Mono.just(search)
                .flatMap(cat -> {
                    if(cat.isBlank() || !cat.equals("byId")) {
                        return Mono.error(() -> new MessageNotValidException("category doesn't exist"));
                    }

                    return service.getById(value);
                });
    }*/

    @GetMapping(
            produces = {MediaType.TEXT_EVENT_STREAM_VALUE})
    public Flux<MessageBoundary> getPage(
            @RequestParam(name = "size", required = false, defaultValue = "10") int size,
            @RequestParam(name = "page", required = false, defaultValue = "0") int page,
            @RequestParam(name = "search", required = false, defaultValue = "freeform") SearchCategory search,
            @RequestParam(name = "value", required = false, defaultValue = "null") String value) {
        return service.getPage(size, page, search, value);
    }

    @DeleteMapping
    public Mono<Void> cleanup() {
        return service.cleanup();
    }
}
