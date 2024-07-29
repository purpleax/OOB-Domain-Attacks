from flask import Flask, request

app = Flask(__name__)

@app.route('/<path:path>', methods=['GET', 'POST'])
def catch_all(path):
    """Catch-all endpoint to log data from any path."""
    data = request.args.get('data') or request.form.get('data')
    print(f"Request to /{path} with data: {data}")
    if data:
        print(f"Received data on /{path}: {data}")
    else:
        print(f"Received request on /{path} with no data.")
    return f'Request received on /{path}', 200

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=80)
