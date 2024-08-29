# Ping Monitor Web Application using Python, Flask, Prometheus, and Grafana

**Ping Monitor** is a web application that enables real-time monitoring of network performance. It allows users to configure pings, collect metrics such as packets sent/received, packet loss, and round-trip time, and store them in a Prometheus time-series database. Grafana is used to visualize these metrics, providing valuable insights into network health and performance.

## System Design Diagram

<img src="https://github.com/Areefin1/Synthetic-Monitoring-Tool/raw/main/ping_monitor_system_architecture.png" alt="Ping Monitor System Architecture" width="500"/>

## Installation Guide

Follow these step-by-step instructions to set up the Ping Monitor web application:

### Prerequisites

1. **Install Python:**
   - Download and install the latest version of Python from the [official Python website](https://www.python.org/downloads/).

2. **Install Prometheus Client:**
   - Download Prometheus from the [Prometheus download page](https://prometheus.io/download/).
   - Extract the downloaded ZIP file and rename the extracted folder to `prometheusfolder`.
   - Replace the default `prometheus.yml` file inside the `prometheusfolder` with the customized version from this repository: [prometheus.yml](https://github.com/Areefin1/Synthetic-Monitoring-Tool/blob/main/prometheusfolder/prometheus.yml).

3. **Import Grafana Visualization Dashboard:**
   - After installing Grafana, log in to the Grafana dashboard. The default credentials are typically set to **admin/admin**. For security reasons, please change the password immediately upon first login. For more details, refer to the [Grafana Authentication Documentation](https://grafana.com/docs/grafana/latest/setup-grafana/configure-security/configure-authentication/#grafana-authentication).
   - Use Grafana to import the visualization dashboard and connect it to Prometheus for real-time monitoring.


### Step-by-Step Setup

1. **Clone the Repository:**
   ```bash
   git clone https://github.com/Areefin1/Synthetic-Monitoring-Tool.git
   cd Synthetic-Monitoring-Tool

2. **Configure PowerShell Execution Policy:**
- Set the execution policy to allow running scripts:
   ```bash
   Set-ExecutionPolicy RemoteSigned -Scope CurrentUser
3. **Create and Activate a Virtual Environment:**
   ```bash
   python -m venv venv
   venv\Scripts\activate
4. **Install Required Python Packages:**
- Install all necessary dependencies from the `requirements.txt` file:
   ```bash
   pip install -r requirements.txt
5. **Run the Flask Application:**
   ```bash
   python flask_app.py
6. **Import Grafana Visualization Dashboard:**
- Use Grafana to import the visualization dashboard and connect it to Prometheus for real-time monitoring.
