from flask import Flask, jsonify, request
from energy_model import PhotovoltaicEnergyModel
from collections import deque
import threading
import time
import math

app = Flask(__name__)

# =========================================================
# CONTROLE DE PROCESSOS
# =========================================================

QUEUE = deque()
RUNNING = set()
HISTORY = []   # histórico de coletas (5 em 5 minutos)

# =========================================================
# PARÂMETROS DA MÁQUINA (CONSUMO)
# =========================================================

P_IT = 1.4        # kW — potência computacional
alpha = 0.4       # fator térmico
M_total = 64      # GB — memória

def machine_consumption():
    """
    Consumo total da máquina:
    L = P_IT + alpha * P_IT
    """
    return P_IT + alpha * P_IT

# =========================================================
# PARÂMETROS FOTOVOLTAICOS (3 CÉLULAS)
# =========================================================

E_init = 10       # kWh
E_max = 50        # kWh

panel_areas = [20, 15, 15]  # três células fotovoltaicas (m²)
eta = 0.18                  # eficiência

pv_model = PhotovoltaicEnergyModel(
    E_init=E_init,
    E_max=E_max,
    panel_areas=panel_areas,
    efficiency=eta
)

# =========================================================
# MODELO DE IRRADIÂNCIA SOLAR
# =========================================================

def solar_irradiance():
    """
    I(t) = max(0, sin(wt))
    """
    t = time.time() % 60
    return max(0, math.sin(t / 60 * math.pi)) * 2

# =========================================================
# LOOP DE GERAÇÃO SOLAR
# =========================================================

def solar_loop():
    while True:
        pv_model.generate(solar_irradiance())
        time.sleep(2)

def monitor_loop():
    """
    Armazena dados da simulação a cada 5 minutos
    (300 segundos).
    """
    while True:
        snapshot = {
            "timestamp": time.strftime("%Y-%m-%d %H:%M:%S"),
            "stored_energy_kwh": pv_model.available_energy(),
            "generation_by_cell_kw": pv_model.generation_by_cell(),
            "total_generation_kw": sum(pv_model.generation_by_cell()),
            "machine_consumption_kw": machine_consumption(),
            "running_processes": list(RUNNING),
            "queued_processes": list(QUEUE)
        }

        HISTORY.append(snapshot)

        # opcional: limitar histórico (ex: últimas 24h = 288 registros)
        if len(HISTORY) > 288:
            HISTORY.pop(0)

        time.sleep(300)  


threading.Thread(target=solar_loop, daemon=True).start()
threading.Thread(target=monitor_loop, daemon=True).start()


# =========================================================
# API – SIMULAÇÃO DE INTEGRAÇÃO COM O WRENCH
# =========================================================

@app.route("/register", methods=["POST"])
def register():
    QUEUE.append(request.json["id"])
    return jsonify({"registered": True})

@app.route("/schedule", methods=["GET"])
def schedule():
    if not QUEUE:
        return jsonify({"scheduled": None})

    process = QUEUE.popleft()
    required_energy = machine_consumption()

    if pv_model.available_energy() >= required_energy:
        pv_model.E -= required_energy
        RUNNING.add(process)
        QUEUE.append(process)
        return jsonify({
            "scheduled": process,
            "running_processes": list(RUNNING),
            "energy_kwh": pv_model.available_energy(),
            "consumption_kw": required_energy,
            "generation_by_cell_kw": pv_model.generation_by_cell()
        })

    QUEUE.append(process)
    return jsonify({
        "scheduled": None,
        "reason": "INSUFFICIENT_SOLAR_ENERGY",
        "running_processes": list(RUNNING),
        "energy_kwh": pv_model.available_energy(),
        "generation_by_cell_kw": pv_model.generation_by_cell()
    })

@app.route("/solar", methods=["GET"])
def solar():
    """
    Endpoint compatível com simuladores (ex: Wrench)
    """
    return jsonify({
        "panel_areas_m2": panel_areas,
        "efficiency": eta,
        "generation_by_cell_kw": pv_model.generation_by_cell(),
        "stored_energy_kwh": pv_model.available_energy()
    })

@app.route("/monitor", methods=["GET"])
def monitor():
    return jsonify({
        "current": {
            "stored_energy_kwh": pv_model.available_energy(),
            "generation_by_cell_kw": pv_model.generation_by_cell(),
            "total_generation_kw": sum(pv_model.generation_by_cell()),
            "machine_consumption_kw": machine_consumption(),
            "running_processes": list(RUNNING),
            "queued_processes": list(QUEUE)
        },
        "history_5min": HISTORY
    })

# =========================================================
# START DO SERVIÇO
# =========================================================

app.run(host="0.0.0.0", port=5000)