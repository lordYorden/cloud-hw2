package hello;

import reactor.core.publisher.Flux;
import reactor.core.publisher.Mono;

public interface ReactiveMessageService {
    public Mono<MessageBoundary> create (MessageBoundary input);
    //public Mono<MessageBoundary> getById (String id);
    //public Mono<Void> updateById (String id, MessageBoundary update);
    public Flux<MessageBoundary> getPage (int size, int page, SearchCategory search, String value);
    public Mono<Void> cleanup();
}
