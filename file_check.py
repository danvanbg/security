import time
import logging
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler
from tqdm import tqdm
import os

# Configure logging
logging.basicConfig(level=logging.DEBUG, format='%(asctime)s [%(levelname)s] %(message)s')

# Directory to monitor
monitor_dir = "/Users/danvan/logs"

# Check if the directory exists
if not os.path.exists(monitor_dir):
    logging.error(f"Directory {monitor_dir} does not exist!")
    exit(1)

# Progress bar total time
total_time = 100  # Total ticks for progress bar (simulated)
progress_interval = 1  # Interval to update progress (can be adjusted)

# Event handler for file system events
class MyHandler(FileSystemEventHandler):
    def on_modified(self, event):
        # Here you can handle events like file modifications
        logging.info(f"Modified file: {event.src_path}")

# Set up observer
observer = Observer()
handler = MyHandler()

observer.schedule(handler, monitor_dir, recursive=False)
observer.start()

try:
    # Progress bar for monitoring task
    with tqdm(total=total_time, desc="Monitoring Progress", unit="tick") as pbar:
        logging.info(f"Monitoring directory: {monitor_dir}")

        # Simulate a task and update the progress bar
        for _ in range(total_time):
            time.sleep(0.1)  # Simulate some processing time
            pbar.update(1)  # Update progress by 1 tick

        logging.info("Progress complete!")

finally:
    # Stop the observer and exit
    observer.stop()
    observer.join()  # Wait for the observer to stop
    logging.info("Observer has stopped and the script is exiting.")
