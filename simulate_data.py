import pandas as pd
import numpy as np

data = []

# Normal behavior
for i in range(300):

    movement = np.random.uniform(0.5, 2.0)
    audio = np.random.uniform(0.3, 1.0)
    duration = np.random.uniform(0, 60)

    freeze = 0

    data.append([movement, audio, duration, freeze])


# Freeze behavior
for i in range(100):

    movement = np.random.uniform(0.0, 0.1)
    audio = np.random.uniform(0.0, 0.2)
    duration = np.random.uniform(120, 300)

    freeze = 1

    data.append([movement, audio, duration, freeze])


df = pd.DataFrame(data,
columns=[
"movement",
"audio",
"duration",
"freeze"
])

df.to_csv("sensor_data.csv",index = False)

print("Dataset Created")