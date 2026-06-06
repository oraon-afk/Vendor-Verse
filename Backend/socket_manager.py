import socketio

# Create a Socket.IO server
# cors_allowed_origins="*" allows all origins (for development)
# In production, specify the actual frontend URL
sio = socketio.AsyncServer(async_mode='asgi', cors_allowed_origins="*")

# Create an ASGI app
socket_app = socketio.ASGIApp(sio)

@sio.event
async def connect(sid, environ):
    print(f"Client connected: {sid}")
    await sio.emit('message', {'data': 'Connected to Supplier Sentinel Real-time Server'}, to=sid)

@sio.event
async def disconnect(sid):
    print(f"Client disconnected: {sid}")

@sio.event
async def message(sid, data):
    print(f"Message from {sid}: {data}")
    # Echo back
    await sio.emit('response', {'data': f"Server received: {data}"}, to=sid)
