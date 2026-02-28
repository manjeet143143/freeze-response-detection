from flask import Flask, request, jsonify

app = Flask(__name__)

sensor_data = {
    "movement": 1.0,
    "audio": 0.5,
    "duration": 10
}

@app.route('/update', methods = ['POST'])
def update():

    global sensor_data

    sensor_data = request.json

    return jsonify({"status":"received"})


@app.route('/data')
def data() :

    return jsonify(sensor_data)


if __name__ == '__main__':

    app.run(host = "0.0.0.0", port = 5050)