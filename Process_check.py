import psutil
import time

# Allowed processes
allowed_processes = ["Finder", "python", "Google Chrome", "Safari"]

def check_processes():
    # Check all running processes
    for proc in psutil.process_iter(['pid', 'name']):
        if proc.info['name'] not in allowed_processes:
            print(f"Warning: Unauthorized process found! {proc.info['name']} (PID: {proc.info['pid']})")
            try:
                proc.terminate()  # Terminate unauthorized processes
                print(f"Terminated: {proc.info['name']}")
            except (psutil.NoSuchProcess, psutil.AccessDenied):
                print(f"Could not terminate process {proc.info['name']}")

if __name__ == "__main__":
    while True:
        check_processes()
        time.sleep(10)  # Check every 10 seconds
