import os
from . import create_app, socketio
from .sensors.sockets import bp as sensors_bp

app = create_app(os.getenv("APP_CONFIG", "production"))

app.register_blueprint(sensors_bp)
# Import models to ensure they're registered
from .buildings.models import Building
from .sensors.models import Sensor, SensorData
from .subscriptions.models import Subscription, Alerts

@app.route('/')
def hello():
    return "Hello World!"

if __name__ == "__main__":
    socketio.run(app)