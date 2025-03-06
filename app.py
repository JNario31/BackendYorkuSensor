import os

from . import create_app

app = create_app(os.getenv("APP_CONFIG", "production"))

# Import models to ensure they're registered
from .buildings.models import Building
from .sensors.models import Sensor, SensorData

@app.route('/')
def hello():
    return "Hello World!"

if __name__ == "__main__":
    app.run()