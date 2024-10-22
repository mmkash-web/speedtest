from flask import Flask, render_template, jsonify
import speedtest
import threading
import time

app = Flask(__name__)

# Use a dictionary to store speed data
speed_data = {"download": 0, "upload": 0}

def run_speed_test():
    global speed_data
    st = speedtest.Speedtest()
    st.get_best_server()
    speed_data['download'] = st.download() / 1_000_000  # Convert to Mbps
    speed_data['upload'] = st.upload() / 1_000_000  # Convert to Mbps

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
    # Use host and port as per Heroku requirements
    app.run(host='0.0.0.0', port=int(os.environ.get('PORT', 5000)))
