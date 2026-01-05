package hello;


import org.springframework.boot.CommandLineRunner;
import org.springframework.context.annotation.Profile;
import org.springframework.stereotype.Component;
import reactor.core.publisher.Flux;

@Component
@Profile("reset")
public class MongoReset implements CommandLineRunner {

    private final ReactiveMessageService service;

    public MongoReset(ReactiveMessageService service) {
        this.service = service;
    }

    @Override
    public void run(String... args) throws Exception {
        service.cleanup()
                .thenMany(Flux.range(1, 3))
                .map(i -> new MessageBoundary(
                        "target@gmail.com",
                        "sender@gmail.com",
                        "message #" + i))
                .flatMap(service::create)
                .collectList()
                .block();
    }
}
