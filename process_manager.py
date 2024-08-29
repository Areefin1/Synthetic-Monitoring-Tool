# Create a new module named `process_manager.py`
# process_manager.py
class ProcessManager:
    def __init__(self):
        self.prometheus_pid = None
        self.pingparser_pid = None

# Singleton instance
process_manager = ProcessManager()
