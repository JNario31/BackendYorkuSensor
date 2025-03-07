from .controllers import create_building, delete_building
from .. import socketio

@socketio.on('message')
def handle_message(data):
    print('received message: ' + str(data))
    socketio.emit('message', "hello")

@socketio.on('connect')
def handle_connect():
    print('Client connected')

@socketio.on('disconnect')
def handle_disconnect():
    print('Client disconnected')

@socketio.on('add_building')
def handle_create_building(data):
    result = create_building(data)
    socketio.emit('building_add', result)

@socketio.on('delete_building')
def handle_delete_building(data):
    result = delete_building(data)
    socketio.emit('building_deleted', result)