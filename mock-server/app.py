from flask import Flask, request, jsonify, abort
import json
import os

app = Flask(__name__)
DATA_FILE = os.path.join(os.path.dirname(__file__), 'data', 'customers.json')

def load_data():
    if not os.path.exists(DATA_FILE):
        return []
    with open(DATA_FILE, 'r') as f:
        return json.load(f)

@app.route('/api/health', methods=['GET'])
def health():
    return jsonify({"status": "healthy"}), 200

@app.route('/api/customers', methods=['GET'])
def get_customers():
    data = load_data()
    
    # Pagination support
    try:
        page = int(request.args.get('page', 1))
        limit = int(request.args.get('limit', 10))
    except ValueError:
        return jsonify({"error": "Invalid pagination parameters"}), 400

    start = (page - 1) * limit
    end = start + limit
    
    return jsonify({
        "data": data[start:end],
        "total": len(data),
        "page": page,
        "limit": limit
    }), 200

@app.route('/api/customers/<string:id>', methods=['GET'])
def get_customer(id):
    data = load_data()
    customer = next((c for c in data if str(c['customer_id']) == id), None)
    
    if not customer:
        abort(404, description="Customer not found")
        
    return jsonify(customer), 200

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)