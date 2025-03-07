from .controllers import create_sensor, delete_sensor
from .. import socketio

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
    