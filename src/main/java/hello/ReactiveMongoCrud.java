package hello;

import org.springframework.data.domain.Pageable;
import org.springframework.data.mongodb.repository.ReactiveMongoRepository;
import org.springframework.data.repository.query.Param;
import reactor.core.publisher.Flux;

public interface ReactiveMongoCrud extends ReactiveMongoRepository<MessageEntity, String> {

    public Flux<MessageEntity> getAllByIdNotNull(Pageable pageable);
    public Flux<MessageEntity> getAllByTarget(@Param("target") String target, Pageable pageable);
    public Flux<MessageEntity> getAllBySender(@Param("sender") String sender, Pageable pageable);
    public Flux<MessageEntity> getAllByUrgentIsTrue(Pageable pageable);
    public Flux<MessageEntity> getAllByUrgentIsTrueAndTarget(@Param("target") String target, Pageable pageable);
    public Flux<MessageEntity> getAllByUrgentIsTrueAndSender(@Param("sender") String sender, Pageable pageable);
}
