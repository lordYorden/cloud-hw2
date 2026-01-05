package hello;

public enum SearchCategory {
    freeform,
    byRecipient,
    bySender,
    byUrgent,
    byId,
    urgentOnlyByRecipient,
    urgentOnlyBySender;

    public static boolean requireEmailCheck(SearchCategory category) {
        return category != SearchCategory.freeform && category != SearchCategory.byUrgent && category != SearchCategory.byId;
    }
}
