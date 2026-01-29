import time
import requests
import os

PLUGIN = "http://energy-plugin:5000"

PROCESS_ID = os.getenv("PROCESS_ID", "unknown")

# Registrar processo no plugin
requests.post(
    f"{PLUGIN}/register",
    json={"id": PROCESS_ID}
)

while True:
    response = requests.get(f"{PLUGIN}/schedule")
    data = response.json()

    if data.get("scheduled") == PROCESS_ID:
        print(
            "EXECUTANDO |",
            "Processo:", PROCESS_ID,
            "| Energia restante (kWh):", round(data["energy_kwh"], 2),
            "| Consumo (kW):", round(data["consumption_kw"], 2),
            "| Geração por célula (kW):",
            [round(x, 2) for x in data["generation_by_cell_kw"]]
        )
    else:
        print(
            "AGUARDANDO |",
            "Processo:", PROCESS_ID,
            "| Motivo:", data.get("reason"),
            "| Energia (kWh):", round(data["energy_kwh"], 2),
            "| Geração por célula (kW):",
            [round(x, 2) for x in data["generation_by_cell_kw"]]
        )

    time.sleep(2)