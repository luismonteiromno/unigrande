echo "Inicializando o postgreSQL"

while ! nc -z db 5432; do
    sleep 0.1
done

echo "PostgreSQL inicializado"

echo "$@"
