from flask import Flask, render_template, redirect, url_for, request
import webbrowser
from yamlreader import load_config, add_destination, update_interval, delete_destination
from main import start_pingparser, start_prometheus, stop_process
from process_manager import process_manager
import time
import os

# Initialize the Flask app
app = Flask(__name__)

config_file = "config.yaml"
config = load_config(config_file)

@app.route('/shutdown', methods=['POST'])
def shutdown():
    
    print("Shutting down Flask server.")
    os._exit(0)

def open_browser():

    time.sleep(1)
    webbrowser.open('http://127.0.0.1:5000')

@app.route('/start')
def start_servers():
    if process_manager.prometheus_pid is None:
        start_prometheus()
    if process_manager.pingparser_pid is None:
        start_pingparser()

    print(f'From flask_app.py: Process has started. prometheus_pid: {process_manager.prometheus_pid}. pingparser_pid: {process_manager.pingparser_pid}')

    webbrowser.open_new_tab('http://localhost:3000/dashboards')

    return redirect(url_for('home'))

@app.route('/stop')
def stop_servers():
    if process_manager.pingparser_pid:
        stop_process(process_manager.pingparser_pid, 'pingparser')
    if process_manager.prometheus_pid:
        stop_process(process_manager.prometheus_pid, 'prometheus')

    print(f"From flask_app.py: Process has stopped. Both prometheus_pid: {process_manager.prometheus_pid} and pingparser_pid: {process_manager.pingparser_pid} process have been stopped.")

    return redirect(url_for('home'))

@app.route('/restart_ping')
def restart_ping():

    print("Restart ping button is clicked.")
    
    if process_manager.prometheus_pid or process_manager.pingparser_pid:
        stop_servers()
    
    start_servers()

    return redirect(url_for('home'))

# Flask route for the home page
@app.route('/')
def home():
    return render_template('index.html', config=config)

@app.route('/add_destination', methods=['POST'])
def add_dest():
    destination = request.form['destination']
    count = int(request.form['count'])

    if not destination or not count:
        return "Both fields are required.", 400
    
    try:
        count = int(count)
    except ValueError:
        return "Ping count must be a positive number.", 400
    
    add_destination(config, destination, count, config_file)
    return redirect(url_for('home'))

@app.route('/update_interval', methods=['POST'])
def update_interv():
    interval = int(request.form['interval'])
    update_interval(config, interval, config_file)
    return redirect(url_for('home'))

@app.route('/delete_destination', methods=['POST'])
def delete_dest():
    destination = request.form['destination']
    delete_destination(config, destination, config_file)
    return redirect(url_for('home'))

# Main function to run the Flask web server
def main():
    app.run(debug=False, port=5000)

if __name__ == "__main__":
    open_browser()
    main()
