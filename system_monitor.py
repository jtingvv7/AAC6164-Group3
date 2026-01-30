import os
import csv
import psutil
import time
from datetime import datetime

# Ensure logs folder exists 
if not os.path.exists("logs"):
    os.makedirs("logs")

TXT_FILE = "logs/system_metrics.txt"
CSV_FILE = "logs/system_metrics.csv"

# Write CSV header if it doesn't exist
if not os.path.isfile(CSV_FILE):
    with open(CSV_FILE, "w", newline="") as f:
        writer = csv.writer(f)
        writer.writerow([
            "timestamp", "cpu_usage", "load1", "load5", "load15",
            "mem_total", "mem_used", "mem_available", "mem_percent",
            "disk_total", "disk_used", "disk_free", "disk_percent",
            "uptime_seconds", "idle_seconds", "total_proc", "running_proc", "sleeping_proc",
            "top_cpu_1", "top_cpu_1_percent", "top_cpu_2", "top_cpu_2_percent", "top_cpu_3", "top_cpu_3_percent",
            "top_mem_1", "top_mem_1_percent", "top_mem_2", "top_mem_2_percent", "top_mem_3", "top_mem_3_percent"
        ])

def get_top_processes(key, limit=3):
    processes = []
    # Identify top processes by CPU or Memory 
    for p in psutil.process_iter(['name', 'cpu_percent', 'memory_percent']):
        try:
            processes.append(p.info)
        except (psutil.NoSuchProcess, psutil.AccessDenied):
            pass
    return sorted(processes, key=lambda x: x[key], reverse=True)[:limit]

def top_list(lst, key):
    result = []
    for i in range(3):
        if i < len(lst):
            result.extend([lst[i]['name'], lst[i][key]])
        else:
            # Adds placeholders if fewer than 3 processes are found
            result.extend(["N/A", 0.0])
    return result

def start_system_monitor():
    print("Monitoring started. Press Ctrl+C to stop.")
    while True:
        now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

        # CPU Metrics 
        cpu_usage = psutil.cpu_percent(interval=1)
        load1, load5, load15 = psutil.getloadavg()

        # Memory Metrics 
        mem = psutil.virtual_memory()

        # Disk Metrics 
        disk = psutil.disk_usage('/')

        # Uptime and Idle Time via /proc/uptime 
        with open("/proc/uptime") as f:
            uptime_seconds, idle_seconds = map(float, f.readline().split())

        # Process Metrics
        processes_list = list(psutil.process_iter(['status']))
        total_proc = len(processes_list)
        running = len([p for p in processes_list if p.info['status'] == psutil.STATUS_RUNNING])
        sleeping = len([p for p in processes_list if p.info['status'] == psutil.STATUS_SLEEPING])

        # Top 3 Processes 
        top_cpu = get_top_processes('cpu_percent')
        top_mem = get_top_processes('memory_percent')

        # Writing to TXT Log for Reporting
        with open(TXT_FILE, "a") as f:
            f.write(f"\n[{now}]\n")
            f.write(f"CPU Usage: {cpu_usage}%\n")
            f.write(f"Load Avg (1,5,15): {load1}, {load5}, {load15}\n")
            f.write(f"Memory: Total: {mem.total}, Used: {mem.used}, Available: {mem.available} ({mem.percent}%)\n")
            f.write(f"Disk: Total: {disk.total}, Used: {disk.used}, Free: {disk.free} ({disk.percent}%)\n")
            f.write(f"Uptime: {int(uptime_seconds)}s, Idle Time: {int(idle_seconds)}s\n")
            f.write(f"Total Processes: {total_proc}, Running: {running}, Sleeping: {sleeping}\n")
            # Optional: Add Top Processes to TXT for completeness
            f.write(f"Top CPU: {[(p['name'], p['cpu_percent']) for p in top_cpu]}\n")
            f.write(f"Top Mem: {[(p['name'], p['memory_percent']) for p in top_mem]}\n")

        # Construct row for CSV
        row = [
            now, cpu_usage, load1, load5, load15,
            mem.total, mem.used, mem.available, mem.percent,
            disk.total, disk.used, disk.free, disk.percent,
            int(uptime_seconds), int(idle_seconds),
            total_proc, running, sleeping
        ] + top_list(top_cpu, 'cpu_percent') + top_list(top_mem, 'memory_percent')

        with open(CSV_FILE, "a", newline="") as f:
            csv.writer(f).writerow(row)

        print(f"[{now}] System metrics recorded")
        time.sleep(10)

if __name__ == "__main__":
    start_system_monitor()
