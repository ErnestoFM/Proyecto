FROM rabbitmq:3.12-management-alpine

# Habilitar plugins necesarios
RUN rabbitmq-plugins enable --offline rabbitmq_management rabbitmq_prometheus

# Copiar configuraciones y definiciones de topología
COPY docker/rabbitmq/definitions.json /etc/rabbitmq/definitions.json

# Configuración de inicio con definiciones automáticas
RUN echo "management.load_definitions = /etc/rabbitmq/definitions.json" >> /etc/rabbitmq/rabbitmq.conf

EXPOSE 5672 15672
