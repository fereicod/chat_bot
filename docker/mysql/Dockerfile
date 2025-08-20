FROM mysql:8.0

COPY init.sql /docker-entrypoint-initdb.d/init.sql
COPY run-init.sh /docker-entrypoint-initdb.d/run-init.sh

RUN chmod +x /docker-entrypoint-initdb.d/run-init.sh