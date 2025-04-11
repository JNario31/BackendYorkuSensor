from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from .config import config
from flask_socketio import SocketIO
from flask_cors import CORS  # Add this import


db = SQLAlchemy()
migrate = Migrate()
socketio = SocketIO()

def create_app(config_mode='production'):
    app = Flask(__name__)
    app.config.from_object(config[config_mode])

 
    CORS(app)
    socketio.init_app(app, cors_allowed_origins="*")



    db.init_app(app)
    migrate.init_app(app, db)
    
    from .buildings import sockets
    from .sensors import sockets
    from .subscriptions import sockets

    # Import models to ensure they're registered with SQLAlchemy
    with app.app_context():
        # Import models
        from .buildings.models import Building
        from .sensors.models import Sensor, SensorData
        from .subscriptions.models import Subscription, Alerts
    
    return app