FROM rabbitmq:3-management

# Define environment variables.
ENV RABBITMQ_USER user
ENV RABBITMQ_PASSWORD user
ENV RABBITMQ_PID_FILE /var/lib/rabbitmq/mnesia/rabbitmq

COPY setupEnvironment/utils/init_rabbitmq.sh /init_rabbitmq.sh
RUN chmod +x /init_rabbitmq.sh

# Define default command
CMD ["/init_rabbitmq.sh"]