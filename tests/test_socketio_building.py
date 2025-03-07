import socketio
import time

# Create a Socket.IO client
sio = socketio.Client()

# Define event handlers
@sio.event
def connect():
    print("Connected to the Socket.IO server!")

@sio.event
def connect_error(error):
    print(f"Connection error: {error}")

@sio.event
def disconnect():
    print("Disconnected from the Socket.IO server")

# Handler for 'message' events from the server
@sio.on('message')
def on_message(data):
    print(f"Received message: {data}")

# Handler for 'building_result' event
@sio.on('building_result')
def on_building_result(data):
    print(f"Received building result: {data}")

# Handler for 'building_destroyed' event
@sio.on('building_destroyed')
def on_building_destroyed(data):
    print(f"Received destroy building result: {data}")
    

# Main function
def run_test():
    server_url = 'http://localhost:4000'
    print(f"Attempting to connect to {server_url}...")
    
    try:
        # Connect to the server with explicit websocket transport
        sio.connect(server_url, transports=['websocket'])
        
        # Send a few test messages
        for i in range(1, 4):
            test_message = f"Test message #{i}"
            print(f"Sending: {test_message}")
            sio.emit('message', test_message)
            time.sleep(2)

        # Send a test add_building request
        test_building_data = {"name": "Test_Lab"}
        print(f"Sending add_building event with data: {test_building_data}")
        sio.emit('add_building', test_building_data)
        
        # Wait a bit to receive any responses
        print("Waiting for responses...")
        time.sleep(5)

        #Send a test to delete_building request
        print(f"Sending delete_building event with data: {test_building_data}")
        sio.emit('delete_building', test_building_data)

        # Wait a bit to receive any responses
        print("Waiting for responses...")
        time.sleep(5)
        
    except Exception as e:
        print(f"Error: {e}")
    
    finally:
        # Disconnect if connected
        if sio.connected:
            print("Disconnecting...")
            sio.disconnect()

if __name__ == "__main__":
    run_test()