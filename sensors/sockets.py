from .controllers import add_sensor_data, create_sensor, delete_sensor, get_sensor_data, get_sensor_id, get_building_sensors
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

