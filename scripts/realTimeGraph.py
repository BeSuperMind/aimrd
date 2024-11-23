import pandas as pd
import matplotlib.pyplot as plt

def PlotGraph():
    # Update the file path as necessary
    file_path = r"graphHrv.csv"
    df = pd.read_csv(file_path)
    
    # Create the main plot
    fig, ax1 = plt.subplots(figsize=(12, 7))
  
    bar_colors = ["#1f77b4" if condition == 0 else "#d62728" for condition in df["condition"]]
    
    # Bar plot for RMSSD values with conditional colors
    ax1.bar(df.index, df["RMSSD"], color=bar_colors, alpha=0.8, width=0.2)
    
    # Add labels and title
    ax1.set_xlabel("Meditation Duration (Intervals)", fontsize=14, fontweight='bold')
    ax1.set_ylabel("RMSSD Values (ms)", fontsize=14, fontweight='bold')
    ax1.set_title("RMSSD Over Meditation Duration", fontsize=16, fontweight='bold')

    
    # Add legend
    calm_patch = plt.Line2D([0], [0], color="#1f77b4", lw=4, label="Calm (Condition = 0)")
    stress_patch = plt.Line2D([0], [0], color="#d62728", lw=4, label="Stressed (Condition = 1)")
    plt.legend(handles=[calm_patch, stress_patch], fontsize=12, loc="upper right")
    
    # Adjust layout and display the plot
    plt.tight_layout()
    plt.show()
