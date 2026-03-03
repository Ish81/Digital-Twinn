# simulation/scenarios.py

import numpy as np

def rainfall_spike(data, start_index, duration=48):
    data = data.copy()
    end_index = min(start_index + duration, len(data))

    # Severe turbidity spike
    data.loc[start_index:end_index, "turbidity"] *= 8

    # Flow surge during rainfall
    data.loc[start_index:end_index, "raw_flow_rate"] *= 1.4

    # Slight pH disturbance
    data.loc[start_index:end_index, "pH"] -= 0.5

    return data


def sudden_pH_drop(data, start_index, duration=24):
    data = data.copy()
    end_index = min(start_index + duration, len(data))
    data.loc[start_index:end_index, "pH"] -= 1.2
    return data


def hardness_surge(data, start_index, duration=24):
    data = data.copy()
    end_index = min(start_index + duration, len(data))
    data.loc[start_index:end_index, "hardness"] *= 1.6
    return data


def sensor_noise(data, percent=0.02):
    data = data.copy()
    n = len(data)
    indices = np.random.choice(n, int(n * percent), replace=False)
    data.loc[indices, "turbidity"] *= 1.4
    return data