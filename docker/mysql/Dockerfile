FROM mysql:8.0

COPY init.sql reset.sql /docker-entrypoint-initdb.d/
COPY run-reset.sh /docker-entrypoint-initdb.d/run-reset.sh

RUN chmod +x /docker-entrypoint-initdb.d/run-reset.sh
