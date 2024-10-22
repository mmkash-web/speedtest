import logging
from flask import Flask, render_template, jsonify
import speedtest
import threading
import os

app = Flask(__name__)

# Configure logging
logging.basicConfig(level=logging.INFO)

speed_data = {"download": 0, "upload": 0}

def run_speed_test():
    global speed_data
    try:
        st = speedtest.Speedtest()
        st.get_best_server()
        speed_data['download'] = st.download() / 1_000_000  # Convert to Mbps
        speed_data['upload'] = st.upload() / 1_000_000  # Convert to Mbps
        logging.info(f"Download: {speed_data['download']} Mbps, Upload: {speed_data['upload']} Mbps")
    except Exception as e:
        logging.error(f"Error running speed test: {e}")

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/test_speed', methods=['POST'])
def test_speed():
    speed_thread = threading.Thread(target=run_speed_test)
    speed_thread.start()
    return ('', 204)

@app.route('/results')
def results():
    return jsonify(speed_data)

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=int(os.environ.get('PORT', 5000)))
