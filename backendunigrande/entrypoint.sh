#!/bin/bash

echo "Inicializando o postgreSQL"

while ! nc -z dbunigrande 5432; do
    sleep 0.1
done

echo "PostgreSQL inicializado"

dos2unix backendunigrande/entrypoint.sh