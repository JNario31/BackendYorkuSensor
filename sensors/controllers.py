from datetime import datetime
from flask import jsonify
from dateutil.parser import isoparse

from .models import Sensor

def create_sensor_data(data):
    id = data.get('id')
    if not id:
          return jsonify({'error': 'Sensor id is required'}), 400
    
    temperature = data.get('temperature')
    humidity = data.get('humidity')
    pressure = data.get('pressure')
    airflow = data.get('airflow')
    timestamp = data.get('timestamp', datetime.utcnow().isoformat())

    if None in [temperature, humidity, pressure, airflow]:
        return jsonify({'error': 'All fields are required'}), 400
    
    sensor = Sensor.query.get(id)
    if not sensor:
        return jsonify({'error': 'Sensor not found'}), 404
    
    timestamp_parsed = isoparse(timestamp)