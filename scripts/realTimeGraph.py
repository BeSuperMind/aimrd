import pandas as pd
import matplotlib.pyplot as plt

def PlotGraph():
      file_path = r"C:\Users\sam\CODEs\aimrd\graphHrv.csv"
      df = pd.read_csv(file_path)
      fig, ax1 = plt.subplots(figsize=(10, 6))

      ax1.plot(df.index, df["RMSSD"], label="RMSSD", color="blue", marker='o', linewidth=1.5)
      ax1.plot(df.index, df["SDNN"], label="SDNN", color="green", marker='x', linewidth=1.5)
      ax1.set_xlabel("Meditation Duration (Intervals)")
      ax1.set_ylabel("RMSSD / SDNN Values")
      ax1.legend(loc="upper left")
      ax1.grid(True)

      # Create a secondary y-axis to plot stress condition as bars or steps
      ax2 = ax1.twinx()
      ax2.step(df.index, df["condition"], where="mid", color="red", label="Stress Condition", linewidth=1.5)
      ax2.set_ylabel("Stress Condition (0=Calm, 1=Stress)")
      ax2.set_yticks([0, 1])  # Only 0 and 1 for stress condition
      ax2.legend(loc="upper right")

      plt.title("RMSSD, SDNN, and Stress Condition over Meditation Duration")
      plt.show()
