import time
import os
import threading
import datetime
from directory_monitor.monitor import DirectoryMonitor
from system_monitor import start_system_monitor

def main():
    print("Linux Monitoring System Started")
    print("Press Ctrl + C to stop")

    watch_dir = "./test_zone"
    if not os.path.exists(watch_dir):
        os.makedirs(watch_dir)
        print("Created testing directory")

    log_dir = "./logs"
    if not os.path.exists(log_dir):
        os.makedirs(log_dir)
    
    dir_log_file = os.path.join(log_dir,"directory_monitor.txt")

    monitor = DirectoryMonitor(watch_dir)

    # Start system monitor in background
    sys_thread = threading.Thread(target=start_system_monitor, daemon=True)
    sys_thread.start()

    try:
        while True:
            logs = monitor.check_changes()
            if logs:
                print("\nChanges Detected")
                with open(dir_log_file,"a") as f:
                    for log in logs:
                        print(log)
                        timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                        f.write(f"[{timestamp}]\n{log}\n" + "-"*30 + "\n")
            time.sleep(3)

    except KeyboardInterrupt:
        print("\nMonitoring stopped")

if __name__ == "__main__":
    main()
