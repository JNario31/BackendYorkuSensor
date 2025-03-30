import os
from . import create_app, socketio

app = create_app(os.getenv("APP_CONFIG", "production"))


# Import models to ensure they're registered
from .buildings.models import Building
from .sensors.models import Sensor, SensorData
from .subscriptions.models import Subscription

@app.route('/')
def hello():
    return "Hello World!"

if __name__ == "__main__":
    socketio.run(app)