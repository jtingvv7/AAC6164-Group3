import time
import os
from directory_monitor.monitor import DirectoryMonitor

def main():
    print("Linux Monitoring System Started")
    print("Press Ctrl + C to stop")
    
    watch_dir = "./test_zone"
    if not os.path.exists(watch_dir):
        os.makedirs(watch_dir)
        print(f"Create testing directoy")
    
    # directory monitor
    monitor = DirectoryMonitor(watch_dir)
    
    try:
        while True:
            # check every 3s
            logs = monitor.check_changes()

            if logs:
                print("\n Changes Detected")
                for log in logs:
                    print(log)

            time.sleep(3)

    except KeyboardInterrupt:
        print("\n Stopped")

if __name__ == "__main__":
    main()