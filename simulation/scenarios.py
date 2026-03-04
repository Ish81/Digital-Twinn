# simulation/scenarios.py

import numpy as np

def rainfall_spike(data, start_index, duration=48):

    data = data.copy()

    end_index = min(start_index + duration, len(data))

    # Heavy rainfall increases turbidity
    data.loc[start_index:end_index, "turbidity"] *= 6

    # Flow surge
    data.loc[start_index:end_index, "raw_flow_rate"] *= 1.3

    # Increase PAC demand
    data.loc[start_index:end_index, "pac_dose_ppm"] *= 1.2

    # Mark rainfall event
    data.loc[start_index:end_index, "rainfall_event"] = 1

    return data


def sensor_noise(data, percent=0.02):

    data = data.copy()

    n = len(data)

    indices = np.random.choice(n, int(n * percent), replace=False)

    data.loc[indices, "turbidity"] *= 1.3
    data.loc[indices, "sensor_noise_flag"] = 1

    return data