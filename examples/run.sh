# client: localhost:8000
uvicorn examples.hyfed.client:app --port 8000

# server: localhost:8001
uvicorn examples.hyfed.server:app --port 8001

# compensator: localhost:8002
uvicorn examples.hyfed.compensator:app --port 8002

# trigger server to send model
python examples/hyfed/trigger_server.py
