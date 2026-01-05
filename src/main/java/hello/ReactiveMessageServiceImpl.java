package hello;

import org.springframework.data.domain.PageRequest;
import org.springframework.data.domain.Sort;
import org.springframework.stereotype.Service;
import reactor.core.publisher.Flux;
import reactor.core.publisher.Mono;

import java.time.ZonedDateTime;
import java.util.HashMap;
import java.util.Map;

@Service
public class ReactiveMessageServiceImpl implements ReactiveMessageService {

    private final ReactiveMongoCrud messages;

    public ReactiveMessageServiceImpl(ReactiveMongoCrud crud) {
        this.messages = crud;
    }

    @Override
    public Mono<MessageBoundary> create(MessageBoundary input) {
        return Mono.just(input)
                .flatMap(msg -> {
                    if(msg.getTitle() == null || msg.getTitle().isBlank()) {
                        return Mono.error(new MessageNotValidException("title is required"));
                    }

                    if(msg.getSender() == null || msg.getSender().isBlank() || !Utils.IsEmail(msg.getSender())) {
                        return Mono.error(new MessageNotValidException("sender must be a valid email"));
                    }

                    if(msg.getTarget() == null || msg.getTarget().isBlank() || !Utils.IsEmail(msg.getTarget())) {
                        return Mono.error(new MessageNotValidException("target must be a valid email"));
                    }

                    return Mono.just(msg);
                })
                .map(b -> {
                    b.setId(null);
                    b.setPublicationTimestamp(ZonedDateTime.now());
                    b.setMoreDetails(new HashMap<>());

                    return b.toEntity();
                })
                .flatMap(this.messages::save)
                .map(MessageBoundary::new);
    }

    @Override
    public Flux<MessageBoundary> getPage(int size, int page, SearchCategory search, String value) {
        return Mono.just(search)
                .flatMap(cat -> {

                    if(value == null || value.isEmpty()) {
                        return Mono.error(() -> new MessageNotValidException("Missing value for category"));
                    }

                    if(SearchCategory.requireEmailCheck(cat) && !Utils.IsEmail(value)) {
                        return Mono.error(() -> new MessageNotValidException("Not a valid email"));
                    }

                    return Mono.just(cat);
                })
                .flatMapMany(cat -> switch (cat) {
                    case byRecipient -> this.messages.getAllByTarget(
                            value,
                            PageRequest.of(page, size, Sort.Direction.DESC, "publicationTimestamp", "id")
                    );
                    case bySender -> this.messages.getAllBySender(
                            value,
                            PageRequest.of(page, size, Sort.Direction.DESC, "publicationTimestamp", "id")
                    );
                    case byUrgent -> this.messages.getAllByUrgentIsTrue(
                            PageRequest.of(page, size, Sort.Direction.DESC, "publicationTimestamp", "id")
                    );
                    case urgentOnlyByRecipient ->  this.messages.getAllByUrgentIsTrueAndTarget(
                            value,
                            PageRequest.of(page, size, Sort.Direction.DESC, "publicationTimestamp", "id")
                    );
                    case urgentOnlyBySender ->  this.messages.getAllByUrgentIsTrueAndSender(
                        value,
                        PageRequest.of(page, size, Sort.Direction.DESC, "publicationTimestamp", "id")
                    );
                    case freeform -> this.messages.getAllByIdNotNull(
                            PageRequest.of(page, size, Sort.Direction.DESC, "publicationTimestamp", "id")
                    );
                    case byId ->  this.messages.findById(
                            value
                    ).switchIfEmpty(Mono.error(()->new MessageNotFoundException("message with id "+value+" was not found")));
                })
                .map(MessageBoundary::new);
    }

    @Override
    public Mono<Void> cleanup() {
        return this.messages.deleteAll();
    }
}
