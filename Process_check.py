import psutil
import time
from tqdm import tqdm

def check_processes():
    print("Monitoring running processes...")

    suspicious_processes = []
    checked_processes = 0  # Counter for checked processes

    # List of all processes to be checked
    all_processes = []

    while True:
        # Check all running processes
        for proc in psutil.process_iter(['pid', 'name', 'exe', 'cmdline', 'cpu_percent', 'memory_info']):
            try:
                process_info = proc.info
                pid = process_info['pid']
                name = process_info['name']
                exe = process_info['exe']
                cmdline = process_info['cmdline']
                cpu_percent = process_info['cpu_percent']
                memory_info = process_info['memory_info']
                owner = proc.username()  # Get the owner of the process

                # Get the parent process PID if available
                parent_pid = proc.ppid()

                # Check for valid CPU and memory usage values
                if cpu_percent is not None and memory_info is not None:
                    if cpu_percent > 80 or memory_info.rss > 500000000:  # Example checks
                        suspicious_processes.append(process_info)

                # Add the process to the list
                all_processes.append(process_info)

            except (psutil.NoSuchProcess, psutil.AccessDenied, psutil.ZombieProcess):
                continue

        # Break if we check all processes for a while (you can change this condition)
        if len(all_processes) > 100:
            break

        time.sleep(1)  # Adjust the sleep time if needed

    # Set up the progress bar
    with tqdm(total=len(all_processes), desc="Monitoring Processes", dynamic_ncols=True) as pbar:
        pbar.set_postfix({"Suspicious Process Count": len(suspicious_processes)})

        for _ in all_processes:
            pbar.update(1)  # Update progress bar for each process

    # Print suspicious processes at the end, each on a new line
    if suspicious_processes:
        print("\nSuspicious processes detected:")
        for proc in suspicious_processes:
            pid = proc['pid']
            name = proc['name']
            cmdline = proc['cmdline']
            cpu_percent = proc['cpu_percent']
            memory = proc['memory_info'].rss
            try:
                owner = psutil.Process(pid).username()  # Get the owner of the process
            except (psutil.NoSuchProcess, psutil.AccessDenied, psutil.ZombieProcess):
                owner = "Unknown"

            try:
                parent_pid = psutil.Process(pid).ppid()  # Get the parent PID
                parent_name = psutil.Process(parent_pid).name() if parent_pid else "Unknown"
            except (psutil.NoSuchProcess, psutil.AccessDenied, psutil.ZombieProcess):
                parent_name = "Unknown"

            print(f"\nPID: {pid}\nName: {name}\nOwner: {owner}\nParent PID: {parent_pid} ({parent_name})\nCommand: {cmdline}\nCPU: {cpu_percent}%\nMemory: {memory} bytes\n")
    else:
        print("\nNo suspicious processes detected.")

if __name__ == "__main__":
    check_processes()  # Check processes periodically
