import numpy as np
import pandas as pd

data = pd.read_csv('hrv_stress_data.csv')

def augment_data(df):
    # Scale RMSSD and SDNN by random factors between 0.95 and 1.05
    df['RMSSD'] = df['RMSSD'] * np.random.uniform(0.95, 1.05, size=len(df))
    df['SDNN'] = df['SDNN'] * np.random.uniform(0.95, 1.05, size=len(df))
    return df


augmented_data = augment_data(data)


augmented_data.to_csv('augmented_hrv_data.csv', index=False)

print(augmented_data)
