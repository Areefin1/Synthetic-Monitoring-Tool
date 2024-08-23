from pingparser import main as launch_pingparser
import subprocess
import time

# Main function that only currently executes pingparser.py file. Will continue to add more functionality.
def main():

    # Start the Prometheus server on port 9090
    start_prometheus = ['./prometheusfolder/prometheus', '--config.file=./prometheusfolder/prometheus.yml']
    subprocess.Popen(start_prometheus)

    time.sleep(7)

    launch_pingparser()

    print("Automatically shutting down Prometheus server on port 9090.")

if __name__ == "__main__":
    main()