import matplotlib.pyplot as plt
import os
from django.conf import settings
def PlotGraph(rmssd_values):
    intervals = list(range(1, len(rmssd_values) + 1))  
    bar_colors = [
      "#399918" if value >= 30 else "#D62728" 
      for value in rmssd_values]  
    fig, ax1 = plt.subplots(figsize=(12, 7))
    ax1.bar(intervals, rmssd_values, label="RMSSD", color=bar_colors, alpha=0.8, width=0.4)
    ax1.set_xlabel("Meditation Duration (Intervals)", fontsize=14, fontweight='bold')
    ax1.set_ylabel("RMSSD Values (ms)", fontsize=14, fontweight='bold', color="#97BE5A")
    ax1.set_title("RMSSD Over Meditation Duration", fontsize=16, fontweight='bold')
    ax1.grid(True, which='both', axis='y', linestyle='--', alpha=0.6)
    plt.tight_layout()
    static_dir = os.path.join("static", "graph")
    os.makedirs(static_dir, exist_ok=True)
    file_path = os.path.join(static_dir, "hrv_report.png")
    plt.savefig(file_path)

    return file_path

