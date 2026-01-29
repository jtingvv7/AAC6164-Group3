import time
import os
import threading
import datetime
from directory_monitor.monitor import DirectoryMonitor
from system_monitor import start_system_monitor

try:
    from Analytics_Reporting.data_processor import generate_visual_report
    print("Graphing module loaded successfully")
except ImportError:
    print("Warning: Error.Graphs will not be generated")
    def generate_visual_report():pass

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

    last_report_time = time.time()
    report_interval = 30

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
            current_time = time.time()
            if current_time - last_report_time > report_interval:
                print("\n[System] Updating graphical reports...")
                generate_visual_report()
                last_report_time = current_time
            time.sleep(3)

    except KeyboardInterrupt:
        print("\nMonitoring stopped")
        print("Generating final report before exit...")
        generate_visual_report()
        print("Done.Bye")

if __name__ == "__main__":
    main()
