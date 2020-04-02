CREATE TABLE postgres.public.messages (
    message_id varchar(255) PRIMARY KEY,
    prev_message_id varchar(255),
    context varchar(255),
    body varchar(255),
    status varchar(255),
    destination varchar(255),
    submit_time varchar(255)
);