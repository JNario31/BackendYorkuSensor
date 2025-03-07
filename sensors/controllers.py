from datetime import datetime
from .. import db
from .models import Sensor, SensorData
from dateutil.parser import isoparse

def create_sensor(data):
    sensor_name = data.get('name')
    building_id = data.get('building_id')
    if not sensor_name or not building_id:
        return {'error': 'sensor name or building id is required'}, 400

    if Sensor.query.filter_by(name=sensor_name, building_id=building_id).first():
        return {'error': 'Sensor already exists'}, 400
    
    db.session.add(Sensor(name=sensor_name, building_id=building_id))
    db.session.commit()
    return{'message': 'Sensor added sucessfully'}, 201

def delete_sensor(data):
    sensor_name = data.get('name')
    building_id = data.get('building_id')
    if not sensor_name or not building_id:
        return {'error': 'sensor name or building id is required'}, 400

    existing_sensor = Sensor.query.filter_by(name=sensor_name, building_id=building_id).first()

    if not existing_sensor:
        return {'error': 'Sensor does not exist'}, 404
    
    db.session.delete(existing_sensor)
    db.session.commit()
    return{'message': 'Sensor deleted sucessfully'}, 201

def add_sensor_data(data):
    sensor_id = data.get('sensor_id')
    if not sensor_id:
        return {'error': 'sensor id is required'}, 400
    
    if not Sensor.query.filter_by(id=sensor_id):
        return {'error': 'sensor does not exist'}, 400
    
    db.session.add(SensorData(
        sensor_id=sensor_id,
        temperature=data.get('temperature'),
        humidity=data.get('humidity'),
        pressure=data.get('pressure'),
        airflow=data.get('airflow'),
        timestamp = isoparse(data.get('timestamp', datetime.utcnow().isoformat()))
    ))
    
    return{'message': 'Sensor data added sucessfully'}, 201

    