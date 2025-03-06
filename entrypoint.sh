pip install flask-script

# Initialize migrations if needed
if [ ! -d "migrations" ]; then
    echo "Initializing migrations..."
    python manage.py db init
fi

# Generate migration
echo "Generating migration..."
python manage.py db migrate -m "Auto migration"

# Apply migration
echo "Applying migration..."
python manage.py db upgrade

# Start the application
echo "Starting application..."
flask run --host=0.0.0.0 --port=4000