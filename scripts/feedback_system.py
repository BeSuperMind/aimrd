import time

# Modify the function to include dynamic threshold setting
def provide_feedback(rmssd, baseline_rmssd=None, population="general"):
    """
    Provide feedback based on RMSSD value.
    
    Parameters:
    - rmssd (float): The calculated RMSSD value in milliseconds.
    - baseline_rmssd (float, optional): The user's baseline RMSSD if available.
    - population (str): The target population ("general", "athlete", "older", etc.).
    """
    # Define population-specific stress thresholds (in milliseconds)
    population_thresholds = {
        "general": 30,      # Stress threshold for the general population (ms)
        "athlete": 50,      # Stress threshold for athletes (ms)
        "older": 20,        # Stress threshold for older adults (ms)
        "custom": baseline_rmssd * 0.8 if baseline_rmssd else 25  # Dynamic threshold based on baseline
    }
    
    # Convert RMSSD to milliseconds if it is in seconds (optional, based on data source)
    if rmssd < 1:  # Assuming the value is in seconds, convert it to ms
        rmssd = rmssd * 100

    # Use the threshold based on the population or default to general
    stress_threshold = population_thresholds.get(population, 30)
    
    if rmssd < stress_threshold:
        print(f"Stress detected! RMSSD ({rmssd:.2f} ms) is below the threshold ({stress_threshold} ms).")
        breathing_guidance()
    else:
        print(f"You are calm. RMSSD ({rmssd:.2f} ms) is above the threshold ({stress_threshold} ms). Keep going.")

def breathing_guidance():
    """
    Guide the user through a breathing exercise to reduce stress.
    """
    print("Let's take a few deep breaths together:")
    for _ in range(3):  # Suggest 3 deep breaths
        print("Inhale deeply through your nose for 4 seconds...")
        time.sleep(4)  # Simulating the inhale duration
        print("Hold for 4 seconds...")
        time.sleep(4)  # Simulating the hold duration
        print("Exhale slowly through your mouth for 6 seconds...")
        time.sleep(6)  # Simulating the exhale duration
    print("Great job! You can return to your activity.")

# Example usage with a custom threshold based on the population type
if __name__ == "__main__": 
    rmssd_value = 0.5321  # Example RMSSD value in seconds (replace with actual calculation)
    baseline_rmssd_value = 0.040  # Example baseline RMSSD in seconds (replace with actual baseline if available)
    
    # Provide feedback for a general population
    provide_feedback(rmssd_value, baseline_rmssd=baseline_rmssd_value, population="general")
    
    # Provide feedback for an athlete
    provide_feedback(rmssd_value, baseline_rmssd=baseline_rmssd_value, population="athlete")
