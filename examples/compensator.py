from fastapi import FastAPI, HTTPException

from hyfed import role, asynchttp, datamodel


app = FastAPI()

GROUP_ID = 1
SERVER_HOST = "localhost"
SERVER_PORT = 8001


@app.post("/{group_id}/compensator/{role_id}")
async def aggregate_noises(role_id: int, group_id: int, data: datamodel.Noise):
    if group_id != GROUP_ID:
        raise HTTPException(status_code=403, detail="Group ID is inconsistent")

    print("Compensator aggregate noises")

    # receiving noise from clients
    noise = data.toarray()
    print(f"Received noise from client: {noise}")

    # aggregate client noise by compensator
    comp = role.HyFedCompensator()
    aggregated_noise = comp.aggregate(noise, noise)
    print(f"Aggregated noise: {aggregated_noise}")

    # passing aggregated_noise to server
    server_url = f"http://{SERVER_HOST}:{SERVER_PORT}/1/server/2"
    result = datamodel.Noise(noise=aggregated_noise.tolist()).todict()
    recv_data = await asynchttp.put(server_url, json=result)
    print("Put to server success")

    return {"status": "OK"}
