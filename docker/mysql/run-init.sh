#!/bin/bash
set -e

mysqld --skip-networking --socket=/var/run/mysqld/mysqld.sock &
pid="$!"

until mysqladmin ping -uroot -p"$MYSQL_ROOT_PASSWORD" --socket=/var/run/mysqld/mysqld.sock >/dev/null 2>&1; do
    echo "⏳ Waiting for database..."
    sleep 2
done

echo "🚀 Running schema init..."
mysql -uroot -p"$MYSQL_ROOT_PASSWORD" "$MYSQL_DATABASE" < /docker-entrypoint-initdb.d/init.sql

kill -s TERM "$pid"
wait "$pid"
