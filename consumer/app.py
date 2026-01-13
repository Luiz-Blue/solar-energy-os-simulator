import time
import requests
import os

PLUGIN = "http://energy-plugin:5000"

PROCESS_ID = os.getenv("PROCESS_ID")
ESSENTIAL = os.getenv("ESSENTIAL") == "true"

# registrar no escalonador
requests.post(
    f"{PLUGIN}/register",
    json={
        "id": PROCESS_ID,
        "essential": ESSENTIAL
    }
)

while True:
    response = requests.get(f"{PLUGIN}/schedule")
    data = response.json()

    if data.get("scheduled") == PROCESS_ID:
        print("EXECUTANDO | Energia restante:", data["remaining"])
        time.sleep(1)
    else:
        print("AGUARDANDO | Motivo:", data.get("reason"))
        time.sleep(1)
