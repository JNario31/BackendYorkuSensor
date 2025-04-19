import csv
from io import StringIO
from flask import Blueprint, jsonify, make_response
from .controllers import add_sensor_data, create_sensor, delete_sensor, get_sensor_data, get_sensor_id, get_building_sensors
from .. import socketio
from .models import Sensor, SensorData

bp = Blueprint('routes', __name__)

@socketio.on('connect')
def handle_connect():
    print('Client connected')

@socketio.on('disconnect')
def handle_disconnect():
    print('Client disconnected')

@socketio.on('add_sensor')
def handle_create_sensor(data):
    result_data, status_code = create_sensor(data)
    socketio.emit('sensor_add', {
        'data': result_data,
        'status_code': status_code
    })

@socketio.on('delete_sensor')
def handle_create_sensor(data):
    result_data, status_code = delete_sensor(data)
    socketio.emit('sensor_delete', {
        'data': result_data,
        'status_code': status_code
    })

@socketio.on('add_sensor_data')
def handle_create_sensor(data):
    result_data, status_code = add_sensor_data(data)
    socketio.emit("add_sensor_data", 
        {"data": result_data, 
         "status_code": status_code
    })
    

@socketio.on('get_sensor_id')
def handle_get_sensor_id(data):
    result_data, status_code = get_sensor_id(data)
    socketio.emit('sensor_id', {
        'data': result_data,
        'status_code': status_code
    })

@socketio.on('get_sensor_data')
def handle_get_sensor_data(data):
    result_data, status_code = get_sensor_data(data)
    socketio.emit('sensor_data', {
        'data': result_data,
        'status_code': status_code
    })
    
@socketio.on('get_building_sensors')
def handle_get_building_sensors(data):
    result_data, status_code = get_building_sensors(data)
    socketio.emit('building_sensors',{
        'data': result_data,
        'status_code': status_code
    })

@bp.route('/export/<int:sensor_id>', methods=['GET'])
def export_sensor_data(sensor_id):
    try:
        # Find the building
        sensor = Sensor.query.get(sensor_id)
        if not sensor:
            return jsonify({'error': 'Sensor not found'}), 404

        # Query sensor data for the building
        data = SensorData.query.filter_by(sensor_id=sensor.id).all()
        if not data:
            return jsonify({'error': 'No sensor data available for this building'}), 404

        building_name = sensor.building.name

        # Create a CSV in memory
        csv_file = StringIO()
        csv_writer = csv.writer(csv_file)

        # Write CSV headers
        csv_writer.writerow(['Timestamp', 'Temperature', 'Humidity', 'Pressure', 'Airflow'])

        # Write data rows
        for record in data:
            csv_writer.writerow([
                record.timestamp.isoformat(),
                record.temperature,
                record.humidity,
                record.pressure,
                record.airflow
            ])

        # Create a response with the CSV data
        response = make_response(csv_file.getvalue())
        response.headers['Content-Disposition'] = f'attachment; filename={building_name}_sensor_data.csv'
        response.headers['Content-Type'] = 'text/csv'

        return response
    except Exception as e:
        return jsonify({'error': str(e)}), 500

