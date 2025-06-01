import subprocess
import sys
import time

# Run backend server.py in api/
backend_cmd = [sys.executable, "api/server.py"]

# Run frontend app.py with streamlit in ui/
frontend_cmd = ["streamlit", "run", "ui/app.py"]

try:
    backend_proc = subprocess.Popen(backend_cmd)
    # Wait a moment for backend to start before frontend
    time.sleep(2)
    frontend_proc = subprocess.Popen(frontend_cmd)

    print("Both backend and frontend started. Press Ctrl+C to stop.")

    backend_proc.wait()
    frontend_proc.wait()

except KeyboardInterrupt:
    print("Shutting down processes...")
    backend_proc.terminate()
    frontend_proc.terminate()
