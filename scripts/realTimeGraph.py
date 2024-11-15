import pandas as pd
import matplotlib.pyplot as plt

def PlotGraph():
    file_path = r"C:\Users\sam\CODEs\aimrd\graphHrv.csv"
    df = pd.read_csv(file_path)

    fig, ax1 = plt.subplots(figsize=(12, 7))

    # Plot RMSSD values
    ax1.plot(df.index, df["RMSSD"], label="RMSSD", color="#1f77b4", marker='o', markersize=6, linewidth=2, linestyle='-', alpha=0.8)
    ax1.set_xlabel("Meditation Duration (Intervals)", fontsize=14, fontweight='bold')
    ax1.set_ylabel("RMSSD Values (ms)", fontsize=14, fontweight='bold', color="#1f77b4")
    ax1.set_title("RMSSD and Stress Condition Over Meditation Duration", fontsize=16, fontweight='bold')

    # Add grid to the primary axis
    ax1.grid(True, which='both', axis='y', linestyle='--', alpha=0.6)
    ax1.tick_params(axis='y', labelcolor="#1f77b4")
    ax1.legend(loc="upper left", fontsize=12)

    # Create a secondary y-axis for stress condition (0 or 1)
    ax2 = ax1.twinx()
    ax2.step(df.index, df["condition"], where="mid", color="#d62728", label="Stress Condition", linewidth=2, linestyle="--")
    ax2.set_ylabel("Stress Condition (0=Calm, 1=Stress)", fontsize=14, fontweight='bold', color="#d62728")
    ax2.set_yticks([0, 1])  # Only 0 and 1 for stress condition
    ax2.tick_params(axis='y', labelcolor="#d62728")
    ax2.legend(loc="upper right", fontsize=12)

    # Shading for calm and stress intervals
    calm_intervals = df[df["condition"] == 0].index
    stress_intervals = df[df["condition"] == 1].index
    for interval in calm_intervals:
        ax1.axvspan(interval - 0.5, interval + 0.5, color="#b0e0e6", alpha=0.2)
    for interval in stress_intervals:
        ax1.axvspan(interval - 0.5, interval + 0.5, color="#ffcccb", alpha=0.2)

    # Adjust layout
    plt.tight_layout()

    # Display the graph
    plt.show()
