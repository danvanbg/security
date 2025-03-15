import psutil
import time
import logging
from tqdm import tqdm

# Configure logging
logging.basicConfig(level=logging.DEBUG, format='%(asctime)s [%(levelname)s] %(message)s')

# Criteria for suspicious processes (customize this as needed)
suspicious_keywords = ["malware", "hack", "virus", "trojan"]  # Customize with actual suspicious keywords
suspicious_processes = []

# Progress bar total time
total_time = 100  # Total ticks for progress bar (simulated)
progress_interval = 1  # Interval to update progress (can be adjusted)

# Function to check processes
def check_processes():
    global suspicious_processes
    for proc in psutil.process_iter(['pid', 'name', 'exe', 'cmdline']):
        try:
            # Log the process information
            logging.debug(f"Checking process: {proc.info}")
            cmdline = " ".join(proc.info['cmdline']) if proc.info['cmdline'] else ""
            # Check for suspicious keywords in the command line or name
            if any(keyword.lower() in cmdline.lower() or keyword.lower() in proc.info['name'].lower() for keyword in suspicious_keywords):
                suspicious_processes.append(proc.info)
        except (psutil.NoSuchProcess, psutil.AccessDenied, psutil.ZombieProcess):
            pass

# Progress bar for monitoring processes
with tqdm(total=total_time, desc="Monitoring Processes", unit="tick") as pbar:
    logging.info("Monitoring running processes...")

    # Simulate progress and check processes every time
    for _ in range(total_time):
        time.sleep(0.1)  # Simulate some processing time
        check_processes()  # Check processes periodically
        pbar.update(1)  # Update progress by 1 tick

    logging.info("Process monitoring complete!")

# After progress completes, print suspicious processes
if suspicious_processes:
    logging.info("\nSuspicious processes detected:")
    for proc in suspicious_processes:
        logging.info(f"PID: {proc['pid']}, Name: {proc['name']}, Command: {' '.join(proc['cmdline'])}")
else:
    logging.info("No suspicious processes detected.")
