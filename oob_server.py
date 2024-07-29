from flask import Flask, request

app = Flask(__name__)

@app.route('/log', methods=['GET', 'POST'])
def log():
    data = request.args.get('data') or request.form.get('data')
    if data:
        print(f"Received data: {data}")
    else:
        print("Received request with no data.")
    return 'Data received', 200

@app.route('/<path:path>', methods=['GET', 'POST'])
def catch_all(path):
    print(f"Received request on path: {path}")
    return 'Request received', 200

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
