from flask import Flask, render_template, jsonify, request

app = Flask(__name__)

# 🚌 Bus data stored in memory (no database needed for beginners!)
buses = {
    "BUS-01": {
        "name": "Route A - City Center",
        "lat": 28.6139,
        "lng": 77.2090,
        "status": "Running",
        "driver": "Ramesh Kumar",
        "speed": 42,
        "passengers": 18
    },
    "BUS-02": {
        "name": "Route B - Airport Express",
        "lat": 28.6200,
        "lng": 77.2200,
        "status": "Running",
        "driver": "Suresh Patel",
        "speed": 65,
        "passengers": 31
    },
    "BUS-03": {
        "name": "Route C - School Bus",
        "lat": 28.6050,
        "lng": 77.1980,
        "status": "Stopped",
        "driver": "Vijay Singh",
        "speed": 0,
        "passengers": 24
    }
}

# ─── PAGES ───────────────────────────────────────────────────────────────────

@app.route("/")
def index():
    """Main map page where you track all buses"""
    return render_template("index.html")

@app.route("/admin")
def admin():
    """Admin panel to update bus locations and info"""
    return render_template("admin.html", buses=buses)

# ─── API ENDPOINTS ────────────────────────────────────────────────────────────

@app.route("/api/buses")
def get_buses():
    """Returns all bus data as JSON (used by the map)"""
    return jsonify(buses)

@app.route("/api/update", methods=["POST"])
def update_bus():
    """Admin uses this to update a bus location"""
    data = request.json
    bus_id = data.get("bus_id")

    if bus_id not in buses:
        return jsonify({"error": "Bus not found"}), 404

    # Update only the fields that were sent
    for field in ["lat", "lng", "status", "speed", "passengers", "driver", "name"]:
        if field in data:
            buses[bus_id][field] = data[field]

    return jsonify({"success": True, "bus": buses[bus_id]})

@app.route("/api/add_bus", methods=["POST"])
def add_bus():
    """Admin can add a new bus"""
    data = request.json
    bus_id = data.get("bus_id")
    if not bus_id or bus_id in buses:
        return jsonify({"error": "Invalid or duplicate Bus ID"}), 400

    buses[bus_id] = {
        "name": data.get("name", "New Route"),
        "lat": float(data.get("lat", 28.6139)),
        "lng": float(data.get("lng", 77.2090)),
        "status": "Running",
        "driver": data.get("driver", "Unknown"),
        "speed": 0,
        "passengers": 0
    }
    return jsonify({"success": True})

# ─── RUN ──────────────────────────────────────────────────────────────────────

if __name__ == "__main__":
    print("🚌 Bus Tracker is running!")
    print("👉 Open http://127.0.0.1:5000 to see the map")
    print("👉 Open http://127.0.0.1:5000/admin to manage buses")
    app.run(debug=True)