import pandas as pd
import matplotlib.pyplot as plt
import os

# Paths relative to the root folder (AAC6164-Group3)
LOG_FILE = "logs/system_metrics.csv"
OUTPUT_DIR = "Analytics_Reporting/output_reports"

if not os.path.exists(OUTPUT_DIR):
    os.makedirs(OUTPUT_DIR)

def generate_visual_report():
    try:
        # Step 1: Data Processing - skipping malformed lines
        df = pd.read_csv(LOG_FILE, on_bad_lines='skip')

        # Matching the exact column names from your 'head' command
        avg_cpu = df['cpu_usage'].mean()
        avg_mem = df['mem_percent'].mean()
        max_cpu = df['cpu_usage'].max()

        # Step 2: Generate Summary Text Report
        report_path = f"{OUTPUT_DIR}/summary_report.txt"
        with open(report_path, "w") as f:
            f.write("--- SYSTEM PERFORMANCE SUMMARY ---\n")
            f.write(f"Average CPU Usage: {avg_cpu:.2f}%\n")
            f.write(f"Average Memory Usage: {avg_mem:.2f}%\n")
            f.write(f"Peak CPU Recorded: {max_cpu:.2f}%\n")

        # Step 3: Visualizations
        # CPU Usage Plot
        plt.figure(figsize=(8, 4))
        plt.plot(df.index, df['cpu_usage'], label='CPU %', color='red')
        plt.title('CPU Usage Over Time')
        plt.xlabel('Record Index')
        plt.ylabel('Usage (%)')
        plt.savefig(f"{OUTPUT_DIR}/cpu_plot.png")

        # Memory Usage Plot (using mem_percent)
        plt.figure(figsize=(8, 4))
        plt.plot(df.index, df['mem_percent'], label='Mem %', color='blue')
        plt.title('Memory Usage Over Time')
        plt.xlabel('Record Index')
        plt.ylabel('Usage (%)')
        plt.savefig(f"{OUTPUT_DIR}/mem_plot.png")

        print(f"Success! Reports and plots generated in {OUTPUT_DIR}")

    except Exception as e:
        print(f"Error during processing: {e}")

if __name__ == "__main__":
    generate_visual_report()
