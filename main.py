from flask import Flask, request, jsonify

app = Flask(__name__)
aircraft_registry = {}

# Function to register or update an aircraft
def register_or_update_aircraft(data):
    aircraft_id = data.get('aircraft_id')
    if aircraft_id:
        if aircraft_id in aircraft_registry:
            # If aircraft already registered, update relevant information
            aircraft_registry[aircraft_id]['altitude'] = data.get('altitude', aircraft_registry[aircraft_id]['altitude'])
            aircraft_registry[aircraft_id]['latitude'] = data.get('latitude', aircraft_registry[aircraft_id]['latitude'])
            aircraft_registry[aircraft_id]['longitude'] = data.get('longitude', aircraft_registry[aircraft_id]['longitude'])
            aircraft_registry[aircraft_id]['departure'] = data.get('departure', aircraft_registry[aircraft_id]['departure'])
            aircraft_registry[aircraft_id]['arrival'] = data.get('arrival', aircraft_registry[aircraft_id]['arrival'])
            aircraft_registry[aircraft_id]['callsign'] = data.get('callsign', aircraft_registry[aircraft_id]['callsign'])
            return {"message": f"Aircraft {aircraft_id} information updated successfully"}
        else:
            # If aircraft not registered, register with full data
            aircraft_registry[aircraft_id] = {
                'callsign': data.get('callsign', 'Unknown'),
                'altitude': data.get('altitude', 0),
                'latitude': data.get('latitude', 0.0),
                'longitude': data.get('longitude', 0.0),
                'heading': data.get('heading', 0),
                'speed': data.get('speed', 0),
                'squawk': data.get('squawk', '0000'),
                'connected': data.get('connected', False),  # Default to False if not provided
                'departure': data.get('departure', "N/A"),
                'arrival': data.get('arrival', "N/A"),
                'flight_plan': data.get('flight_plan', "N/A"),
                'cruise_altitude': data.get('cruise', "N/A"),
            }
            return {"message": f"Aircraft {aircraft_id} registered successfully"}
    else:
        return {"error": "Aircraft ID not provided"}, 400

# Function to check if an aircraft is connected
def is_aircraft_connected(aircraft_id):
    return aircraft_registry.get(aircraft_id, {}).get('connected', False)

@app.route('/register_aircraft', methods=['POST'])
def post_endpoint():
    data = request.json
    return jsonify(register_or_update_aircraft(data))

@app.route('/get_aircrafts', methods=['GET'])
def get_aircrafts():
    # Returns information about all registered aircraft
    return jsonify(aircraft_registry)

@app.route('/get_aircraft_info/<aircraft_id>', methods=['GET'])
def get_aircraft_info(aircraft_id):
    # Returns detailed information for a specific aircraft
    if aircraft_id in aircraft_registry:
        aircraft_info = aircraft_registry[aircraft_id]
        aircraft_info['connected'] = is_aircraft_connected(aircraft_id)
        return jsonify(aircraft_info)
    else:
        return jsonify({"error": f"Aircraft {aircraft_id} not found"}), 404

if __name__ == '__main__':
    app.run(debug=True, host="0.0.0.0")
