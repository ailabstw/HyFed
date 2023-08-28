from fastapi import FastAPI, HTTPException

from hyfed import role, asynchttp, datamodel


app = FastAPI()

GROUP_ID = 1
COMPENSATOR_HOST = "localhost"
COMPENSATOR_PORT = 8002
N = 5


@app.post("/{group_id}/client/{role_id}")
async def add_noise_to_model(role_id: int, group_id: int, model: datamodel.ModelParameters):
    if group_id != GROUP_ID:
        raise HTTPException(status_code=403, detail="Group ID is inconsistent")

    print("Client add noise to model")

    parameters = model.toarray()
    print(f"Received model from server: {parameters}")

    # generate noise and noisy model
    client = role.HyFedClient()
    client.update_noise(N)
    noise, noisy_model = client.generate_secrets(parameters)

    # passing noise to compensator
    compensator_url = f"http://{COMPENSATOR_HOST}:{COMPENSATOR_PORT}/1/compensator/3"
    json_noise = datamodel.Noise(noise=noise.tolist()).todict()
    recv_data = await asynchttp.post(compensator_url, json=json_noise)

    # passing noisy_model to server
    result = datamodel.ModelParameters(parameters=noisy_model.tolist()).todict()
    return result
