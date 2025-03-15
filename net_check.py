import os
import psutil
import sys
from tqdm import tqdm

# Function to re-run the script with sudo if not already running as root
def check_sudo():
    if os.geteuid() != 0:
        print("This script needs to be run as root. Re-running with sudo...")
        # Re-run the script with sudo
        os.execvp("sudo", ["sudo", "python3"] + sys.argv)
    else:
        print("Running with sudo privileges.")

def get_process_owner(pid):
    try:
        proc = psutil.Process(pid)
        return proc.username()
    except (psutil.NoSuchProcess, psutil.AccessDenied):
        return "N/A"

def check_network_connections():
    return psutil.net_connections(kind='inet')

def check_processes():
    suspicious_processes = []
    connections = check_network_connections()
    valid_connections = [conn for conn in connections if conn.raddr]  # Filter out invalid connections
    total_connections = len(valid_connections)

    # Progress bar for total connections being checked
    with tqdm(total=total_connections, desc="Checking Processes", unit="conn", ncols=100) as pbar:
        for conn in valid_connections:
            try:
                pid = conn.pid
                if pid is not None:
                    proc = psutil.Process(pid)
                    proc_name = proc.name()
                    owner = get_process_owner(pid)
                    dest_ip = conn.raddr.ip if conn.raddr else "N/A"
                    dest_port = conn.raddr.port if conn.raddr else "N/A"
                    suspicious_processes.append({
                        "PID": pid,
                        "Name": proc_name,
                        "Owner": owner,
                        "Destination IP": dest_ip,
                        "Destination Port": dest_port,
                        "Command": proc.cmdline(),
                    })
            except (psutil.NoSuchProcess, psutil.AccessDenied, psutil.ZombieProcess) as e:
                # Catch AccessDenied and skip the process
                print(f"Access denied for PID {pid}: {str(e)}")
                continue
            pbar.update(1)

    # Show Suspicious processes after check
    return suspicious_processes

def display_suspicious_processes():
    suspicious_processes = check_processes()

    if suspicious_processes:
        print("\nSuspicious processes making network connections:\n")
        for proc in suspicious_processes:
            print(f"PID: {proc['PID']}")
            print(f"Name: {proc['Name']}")
            print(f"Owner: {proc['Owner']}")
            print(f"Destination IP: {proc['Destination IP']}")
            print(f"Destination Port: {proc['Destination Port']}")
            print(f"Command: {' '.join(proc['Command'])}\n")
    else:
        print("\nNo suspicious processes found making network connections.")

if __name__ == "__main__":
    check_sudo()  # Ensure the script is run with sudo
    display_suspicious_processes()
