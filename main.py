import subprocess
import time
import os
import sys
from process_manager import process_manager
import psutil

def start_prometheus():

    with open(os.devnull, 'w') as devnull:
        start_prometheus = ['./prometheusfolder/prometheus', '--config.file=./prometheusfolder/prometheus.yml']
        proc = subprocess.Popen(start_prometheus, stdout=devnull, stderr=devnull)
        process_manager.prometheus_pid = proc.pid
        print(f'From main.py: Prometheus started with PID: {process_manager.prometheus_pid}')

def start_pingparser():

    proc = subprocess.Popen([sys.executable, './pingparser.py'])
    process_manager.pingparser_pid = proc.pid
    print(f'From main.py: Ping parser started with PID: {process_manager.pingparser_pid}')

def stop_process(pid, process_name):

    try:
        process = psutil.Process(pid)
        process.terminate()
        process.wait(timeout=5)
        if process.is_running():
            process.kill()
        print(f'From main.py: Process with PID {pid} stopped.')

        if process_name == 'prometheus':
            process_manager.prometheus_pid = None
        elif process_name == 'pingparser':
            process_manager.pingparser_pid = None
    
    except psutil.NoSuchProcess:
        print(f'From main.py: Process with PID {pid} does not exist.')
        if process_name == 'prometheus':
            process_manager.prometheus_pid = None
        elif process_name == 'pingparser':
            process_manager.pingparser_pid = None
    
    except psutil.AccessDenied:
        print(f'From main.py: Access denied when trying to stop process with PID {pid}')
    except Exception as e:
        print(f'From main.py: Error stopping process with PID {pid}: {e}')

# Main function that only currently executes pingparser.py file. Will continue to add more functionality.
def main():

    # Start the Prometheus server on port 9090
    start_prometheus()

    time.sleep(5)

    start_pingparser()

    print("Process are running. Access the Flask server to control them.")

if __name__ == "__main__":
    main()