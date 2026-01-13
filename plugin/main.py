from flask import Flask, jsonify, request
from energy_model import EnergyModel
from collections import deque
import threading
import time

app = Flask(__name__)

energy = EnergyModel(
    solar_rate=5,
    battery=10,
    battery_max=60
)

QUEUE = deque()
QUANTUM_ENERGY = 10

METRICS = {
    "executions": 0,
    "blocked": 0,
    "energy_used": 0
}

def solar_loop():
    while True:
        energy.generate()
        time.sleep(2)

threading.Thread(target=solar_loop, daemon=True).start()

@app.route("/register", methods=["POST"])
def register():
    data = request.json
    QUEUE.append({
        "id": data["id"],
        "essential": data["essential"]
    })
    return jsonify({"registered": True})

@app.route("/schedule", methods=["GET"])
def schedule():
    if not QUEUE:
        return jsonify({"scheduled": None})

    process = QUEUE.popleft()

    if energy.available_energy() >= QUANTUM_ENERGY:
        energy.consume(QUANTUM_ENERGY)
        METRICS["executions"] += 1
        METRICS["energy_used"] += QUANTUM_ENERGY
        QUEUE.append(process)
        return jsonify({
            "scheduled": process["id"],
            "remaining": energy.available_energy()
        })

    METRICS["blocked"] += 1

    if process["essential"]:
        QUEUE.append(process)
        reason = "WAITING_FOR_ENERGY"
    else:
        reason = "NON_ESSENTIAL_SKIPPED"

    return jsonify({
        "scheduled": None,
        "reason": reason,
        "remaining": energy.available_energy()
    })

@app.route("/metrics", methods=["GET"])
def metrics():
    return jsonify(METRICS)

app.run(host="0.0.0.0", port=5000)
