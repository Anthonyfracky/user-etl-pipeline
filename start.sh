#!/bin/sh
while ! pg_isready -h "$DB_HOST" -p "$DB_PORT" -q; do
    echo "Waiting for database connection..."
    sleep 2
done
echo "Database connected successfully"
alembic upgrade head
python main.py
