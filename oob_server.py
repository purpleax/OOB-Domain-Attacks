from flask import Flask, request

app = Flask(__name__)

@app.route('/log', methods=['GET', 'POST'])
def log():
    """Endpoint specifically for logging data."""
    data = request.args.get('data') or request.form.get('data')
    if data:
        print(f"Received data on /log: {data}")
    else:
        print("Received request on /log with no data.")
    return 'Data received on /log', 200

@app.route('/<path:path>', methods=['GET', 'POST'])
def catch_all(path):
    """Catch-all endpoint to log data from any path."""
    data = request.args.get('data') or request.form.get('data')
    if data:
        print(f"Received data on /{path}: {data}")
    else:
        print(f"Received request on /{path} with no data.")
    return f'Request received on /{path}', 200

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
