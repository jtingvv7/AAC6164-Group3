import pandas as pd
import matplotlib.pyplot as plt
import os

SYS_LOG = "logs/system_metrics.csv"        # cy
DIR_LOG = "logs/directory_monitor.txt"     # joan

OUTPUT_DIR = "logs"  
if not os.path.exists(OUTPUT_DIR):
    os.makedirs(OUTPUT_DIR)

def generate_visual_report():
    print("--- Starting Report Generation ---")

    # system monitor part
    if os.path.exists(SYS_LOG):
        try:
            df = pd.read_csv(SYS_LOG, on_bad_lines='skip')
            
            # CPU Usage
            if 'cpu_usage' in df.columns:
                plt.figure(figsize=(10, 5))
                x_axis = df['timestamp'] if 'timestamp' in df.columns else df.index
                
                plt.plot(x_axis, df['cpu_usage'], color='red', marker='o', label='CPU %')
                plt.title('System CPU Usage Trend')
                plt.xlabel('Time')
                plt.ylabel('Usage (%)')
                plt.xticks(rotation=45) 
                plt.grid(True)
                plt.tight_layout()
                plt.savefig(f"{OUTPUT_DIR}/cpu_report.png")
                print(f"-> Saved: {OUTPUT_DIR}/cpu_report.png")
                plt.close()

            # Memory Usage
            if 'mem_percent' in df.columns:
                plt.figure(figsize=(10, 5))
                x_axis = df['timestamp'] if 'timestamp' in df.columns else df.index

                plt.plot(x_axis, df['mem_percent'], color='blue', marker='x', label='Memory %')
                plt.title('System Memory Usage Trend')
                plt.xlabel('Time')
                plt.ylabel('Memory Usage (%)')
                plt.ylim(0, 100) 
                plt.xticks(rotation=45)
                plt.grid(True)
                plt.tight_layout()
                plt.savefig(f"{OUTPUT_DIR}/memory_report.png")
                print(f"-> Saved: {OUTPUT_DIR}/memory_report.png")
                plt.close()
            else:
                print("Column 'mem_percent' not found in CSV.")

            
        except Exception as e:
            print(f"Error processing System Logs: {e}")
    else:
        print("Warning: system_metrics.csv not found.")

    # directory monitor part
    if os.path.exists(DIR_LOG):
        try:
            stats = {"CREATED": 0, "MODIFIED": 0, "DELETED": 0}
            
            with open(DIR_LOG, "r") as f:
                for line in f:
                    if "[CREATED]" in line:
                        stats["CREATED"] += 1
                    elif "[MODIFIED]" in line:
                        stats["MODIFIED"] += 1
                    elif "[DELETED]" in line:
                        stats["DELETED"] += 1
            
            if sum(stats.values()) > 0:
                labels = [k for k, v in stats.items() if v > 0]
                sizes = [v for v in stats.values() if v > 0]
                colors = ['#4CAF50', '#FFC107', '#F44336'] 
                
                plt.figure(figsize=(6, 6))
                plt.pie(sizes, labels=labels, autopct='%1.1f%%', colors=colors, startangle=140)
                plt.title('File System Activity Distribution')
                plt.savefig(f"{OUTPUT_DIR}/file_activity_report.png")
                print(f"-> Saved: {OUTPUT_DIR}/file_activity_report.png")
                plt.close()
            else:
                print("No file activities recorded yet.")
                
        except Exception as e:
            print(f"Error processing Directory Logs: {e}")
    else:
        print("Warning: directory_monitor.txt not found.")

if __name__ == "__main__":
    generate_visual_report()
