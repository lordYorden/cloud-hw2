package hello;

import java.time.ZoneId;
import java.time.ZonedDateTime;
import java.util.Date;
import java.util.Map;

public class MessageBoundary {
    private String id;
    private String target;
    private String sender;
    private String title;
    private ZonedDateTime publicationTimestamp;
    private boolean urgent;
    private Map<String, Object> moreDetails;

    public MessageBoundary() {
    }

    public MessageBoundary(String target, String sender, String title){
        this.setTarget(target);
        this.setSender(sender);
        this.setTitle(title);
    }

    public MessageBoundary(MessageEntity entity){
        this.setId(entity.getId());
        this.setTarget(entity.getTarget());
        this.setSender(entity.getSender());
        this.setTitle(entity.getTitle());
        this.setUrgent(entity.isUrgent());
        this.setMoreDetails(entity.getMoreDetails());

        this.setPublicationTimestamp(
                ZonedDateTime.ofInstant(
                        entity.getPublicationTimestamp()
                                .toInstant(),
                        ZoneId.systemDefault()));
    }

    public String getId() {
        return id;
    }

    public void setId(String id) {
        this.id = id;
    }

    public String getTarget() {
        return target;
    }

    public void setTarget(String target) {
        this.target = target;
    }

    public String getSender() {
        return sender;
    }

    public void setSender(String sender) {
        this.sender = sender;
    }

    public String getTitle() {
        return title;
    }

    public void setTitle(String title) {
        this.title = title;
    }

    public ZonedDateTime getPublicationTimestamp() {
        return publicationTimestamp;
    }

    public void setPublicationTimestamp(ZonedDateTime publicationTimestamp) {
        this.publicationTimestamp = publicationTimestamp;
    }

    public boolean isUrgent() {
        return urgent;
    }

    public void setUrgent(boolean urgent) {
        this.urgent = urgent;
    }

    public Map<String, Object> getMoreDetails() {
        return moreDetails;
    }

    public void setMoreDetails(Map<String, Object> moreDetails) {
        this.moreDetails = moreDetails;
    }

    public MessageEntity toEntity(){
        MessageEntity rv = new MessageEntity();
        rv.setId(this.getId());
        rv.setSender(this.getSender());
        rv.setTarget(this.getTarget());
        rv.setTitle(this.getTitle());
        rv.setUrgent(this.isUrgent());
        rv.setMoreDetails(this.getMoreDetails());

        rv.setPublicationTimestamp(
                Date.from(
                        this.getPublicationTimestamp()
                                .toInstant()));

        return rv;
    }

    @Override
    public String toString() {
        return "{" +
                "id:'" + id + '\'' +
                ", target:'" + target + '\'' +
                ", sender:'" + sender + '\'' +
                ", title:'" + title + '\'' +
                ", publicationTimestamp:" + publicationTimestamp +
                ", urgent:" + urgent +
                ", moreDetails:" + moreDetails +
                '}';
    }
}
