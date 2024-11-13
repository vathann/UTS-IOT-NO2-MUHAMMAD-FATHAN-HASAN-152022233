from datetime import datetime
from flask import Flask, request, send_file, jsonify
import json
from flask_cors import CORS
from flask import Flask, render_template


app = Flask(__name__)
CORS(app)  # Aktifkan CORS jika diperlukan

database = [
    {
        'idx': 101,
        'suhu': 36,
        'humid': 36,
        'kecerahan': 25,
        'timestamp': '2010-09-18 07:23:48'
    },
    {
        'idx': 226,
        'suhu': 36,
        'humid': 36,
        'kecerahan': 27,
        'timestamp': '2011-05-02 12:29:34'
    },
]

key = max([data['idx'] for data in database], default=0)

@app.route('/')
def index_html():
    return render_template('index.html')

@app.route('/api/post', methods=['POST'])
def post_data():
    global key
    json_data = request.get_json()

    if not request.is_json or not json_data:
        return jsonify({'message': 'data is not json'}), 400

    key += 1
    data = {
        'idx': key,
        'suhu': int(json_data['suhu']),
        'humid': int(json_data['kelembaban']),
        'kecerahan': int(json_data['kecerahan']),
        'timestamp': datetime.now().isoformat()
    }

    database.append(data)

    return jsonify({'message': 'success'}), 200

@app.route('/api/get', methods=['GET'])
def get_data():
    data_suhu = [data['suhu'] for data in database]
    month_year_max = [
        {
            'month_year': datetime.fromisoformat(data['timestamp']).strftime('%m-%Y')
        } for data in database
    ]

    suhumax = max(data_suhu)
    suhumin = min(data_suhu)
    suhurata = sum(data_suhu) / len(data_suhu)

    data = {
        'suhumax': suhumax,
        'suhumin': suhumin,
        'suhurata': suhurata,
        'nilai_suhu_max_humid_max': database,
        'month_year_max': month_year_max
    }

    return jsonify(data)

@app.route('/api/download', methods=['GET'])
def download_json():
    # Membuat file JSON dari database
    file_path = "data.json"
    with open(file_path, 'w') as f:
        json.dump(database, f, indent=4)

    return send_file(file_path, as_attachment=True, download_name="data.json", mimetype='application/json')

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=9990, debug=True)
