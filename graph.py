# Plot stationary vs moving time
import matplotlib.pyplot as plt

def plot_graph(stationary_count, moving_count):
    total_frames = stationary_count + moving_count
    stationary_percentage = (stationary_count / total_frames) * 100 if total_frames > 0 else 0
    moving_percentage = (moving_count / total_frames) * 100 if total_frames > 0 else 0

    # Plot the bar graph
    labels = ['Stationary', 'Moving']
    times = [stationary_percentage, moving_percentage]

    plt.figure(figsize=(6, 4))
    plt.bar(labels, times, color=['green', 'red'])
    plt.xlabel('State')
    plt.ylabel('Time Percentage (%)')
    plt.title('Time Spent Stationary vs Moving')
    plt.ylim(0, 100)
    plt.show()
