import psutil
import time
from datetime import datetime

LOG_FILE = "logs/system_metrics.txt"

def get_top_processes(key, limit=3):
    processes = []
    for p in psutil.process_iter(['pid', 'name', 'cpu_percent', 'memory_percent', 'status']):
        try:
            processes.append(p.info)
        except psutil.NoSuchProcess:
            pass
    return sorted(processes, key=lambda x: x[key], reverse=True)[:limit]

while True:
    now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    cpu_usage = psutil.cpu_percent(interval=1)
    load_avg = psutil.getloadavg()

    mem = psutil.virtual_memory()
    disk = psutil.disk_usage('/')

    boot_time = psutil.boot_time()
    uptime = int(time.time() - boot_time)

    processes = list(psutil.process_iter(['status']))
    total_proc = len(processes)
    running = len([p for p in processes if p.info['status'] == psutil.STATUS_RUNNING])
    sleeping = len([p for p in processes if p.info['status'] == psutil.STATUS_SLEEPING])

    top_cpu = get_top_processes('cpu_percent')
    top_mem = get_top_processes('memory_percent')

    with open(LOG_FILE, "a") as f:
        f.write(f"\n[{now}]\n")
        f.write(f"CPU Usage: {cpu_usage}%\n")
        f.write(f"Load Avg (1,5,15): {load_avg}\n")
        f.write(f"Memory Usage: {mem.percent}%\n")
        f.write(f"Disk Usage: {disk.percent}%\n")
        f.write(f"Uptime (seconds): {uptime}\n")
        f.write(f"Total Processes: {total_proc}, Running: {running}, Sleeping: {sleeping}\n")

        f.write("Top CPU Processes:\n")
        for p in top_cpu:
            f.write(f"  {p['name']} ({p['cpu_percent']}%)\n")

        f.write("Top Memory Processes:\n")
        for p in top_mem:
            f.write(f"  {p['name']} ({p['memory_percent']:.2f}%)\n")

    print(f"[{now}] System metrics recorded")
    time.sleep(10)
