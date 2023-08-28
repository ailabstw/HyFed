import numpy as np

from fastapi import FastAPI, HTTPException

from hyfed import role, asynchttp, datamodel


app = FastAPI()

GROUP_ID = 1
CLIENT_HOST = "localhost"
CLIENT_PORT = 8000
N = 5
model = np.random.rand(N)
noisy_models = []


@app.get("/{group_id}/server/{role_id}")
async def send_model(role_id: int, group_id: int):
    if group_id != GROUP_ID:
        raise HTTPException(status_code=403, detail="Group ID is inconsistent")

    # passing server model to clients
    print(f"Server send model to client: {model}")
    data = datamodel.ModelParameters(parameters=model).todict()
    client_url = f"http://{CLIENT_HOST}:{CLIENT_PORT}/1/client/1"
    recv_data = await asynchttp.post(client_url, json=data)

    # receiving noisy_model from clients
    noisy_model = datamodel.ModelParameters(**recv_data).toarray()
    noisy_models.append(noisy_model)
    print(f"Received noisy model from client: {noisy_model}")
    return {"status": "OK"}


@app.put("/{group_id}/server/{role_id}")
async def update_model(role_id: int, group_id: int, data: datamodel.Noise):
    if group_id != GROUP_ID:
        raise HTTPException(status_code=403, detail="Group ID is inconsistent")

    global model, noisy_models

    # receiving aggregated_noise from compensator
    aggregated_noise = data.toarray()
    print(f"Received aggregated noise from compensator: {aggregated_noise}")

    # aggregate client noisy models and aggregated_noise
    server = role.HyFedServer()
    aggregated_model = server.aggregate(aggregated_noise, *noisy_models)
    model = server.update_model(model, aggregated_model)
    print(f"Updated model: {model}")
    return {"status": "OK"}
