import psutil
import time
from datetime import datetime
import csv
import os


if not os.path.exists("logs"):
    os.makedirs("logs")

TXT_FILE = "logs/system_metrics.txt"
CSV_FILE = "logs/system_metrics.csv"


if not os.path.isfile(CSV_FILE):
    with open(CSV_FILE, "w", newline="") as f:
        writer = csv.writer(f)
        writer.writerow([
            "timestamp", "cpu_usage", "load1", "load5", "load15",
            "mem_total", "mem_used", "mem_available", "mem_percent",
            "disk_total", "disk_used", "disk_free", "disk_percent",
            "uptime_seconds", "total_proc", "running_proc", "sleeping_proc",
            "top_cpu_1", "top_cpu_1_percent", "top_cpu_2", "top_cpu_2_percent", "top_cpu_3", "top_cpu_3_percent",
            "top_mem_1", "top_mem_1_percent", "top_mem_2", "top_mem_2_percent", "top_mem_3", "top_mem_3_percent"
        ])

def get_top_processes(key, limit=3):
    processes = []
    for p in psutil.process_iter(['name', 'cpu_percent', 'memory_percent']):
        try:
            processes.append(p.info)
        except psutil.NoSuchProcess:
            pass
    return sorted(processes, key=lambda x: x[key], reverse=True)[:limit]

def top_list(lst, key):
    result = []
    for i in range(3):
        if i < len(lst):
            result.extend([lst[i]['name'], lst[i][key]])
        else:
            result.extend(["", ""])
    return result

while True:
    now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    cpu_usage = psutil.cpu_percent(interval=1)
    load1, load5, load15 = psutil.getloadavg()

    mem = psutil.virtual_memory()
    disk = psutil.disk_usage('/')

    uptime = int(time.time() - psutil.boot_time())

    processes = list(psutil.process_iter(['status']))
    total_proc = len(processes)
    running = len([p for p in processes if p.info['status'] == psutil.STATUS_RUNNING])
    sleeping = len([p for p in processes if p.info['status'] == psutil.STATUS_SLEEPING])

    top_cpu = get_top_processes('cpu_percent')
    top_mem = get_top_processes('memory_percent')

   
    with open(TXT_FILE, "a") as f:
        f.write(f"\n[{now}]\n")
        f.write(f"CPU Usage: {cpu_usage}%\n")
        f.write(f"Load Avg (1,5,15): {load1}, {load5}, {load15}\n")
        f.write(f"Memory Usage: {mem.percent}% ({mem.used}/{mem.total})\n")
        f.write(f"Disk Usage: {disk.percent}% ({disk.used}/{disk.total})\n")
        f.write(f"Uptime (seconds): {uptime}\n")
        f.write(f"Total Processes: {total_proc}, Running: {running}, Sleeping: {sleeping}\n")
        f.write("Top CPU Processes:\n")
        for p in top_cpu:
            f.write(f"  {p['name']} ({p['cpu_percent']}%)\n")
        f.write("Top Memory Processes:\n")
        for p in top_mem:
            f.write(f"  {p['name']} ({p['memory_percent']:.2f}%)\n")

    row = [
        now, cpu_usage, load1, load5, load15,
        mem.total, mem.used, mem.available, mem.percent,
        disk.total, disk.used, disk.free, disk.percent,
        uptime, total_proc, running, sleeping
    ] + top_list(top_cpu, 'cpu_percent') + top_list(top_mem, 'memory_percent')

    with open(CSV_FILE, "a", newline="") as f:
        writer = csv.writer(f)
        writer.writerow(row)

    print(f"[{now}] System metrics recorded")
    time.sleep(10)

