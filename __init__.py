from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from .config import config
from flask_socketio import SocketIO

db = SQLAlchemy()
migrate = Migrate()
socketio = SocketIO()

def create_app(config_mode='production'):
    app = Flask(__name__)
    app.config.from_object(config[config_mode])
    socketio.init_app(app)

    db.init_app(app)
    migrate.init_app(app, db)
    
    from .buildings import sockets
    from .sensors import sockets

    # Import models to ensure they're registered with SQLAlchemy
    with app.app_context():
        # Import models
        from .buildings.models import Building
        from .sensors.models import Sensor, SensorData
    
    return app