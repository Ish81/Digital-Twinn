# data_generator.py

import numpy as np
import pandas as pd

HOURS = 8760
START_DATE = "2024-01-01"

np.random.seed(42)

# ------------------------
# TIME
# ------------------------
timestamps = pd.date_range(start=START_DATE, periods=HOURS, freq="h")
time = np.arange(HOURS)

# ------------------------
# SEASONAL SIGNAL
# ------------------------
season_cycle = np.sin(2 * np.pi * time / (24 * 365))

# ------------------------
# TEMPERATURE (Pune style)
# ------------------------
temperature = 25 + 6 * season_cycle + np.random.normal(0, 0.5, HOURS)

# ------------------------
# RAINFALL EVENTS
# ------------------------
rainfall_event = np.zeros(HOURS)

for i in range(0, HOURS, 1200):
    if np.random.rand() > 0.6:
        duration = np.random.randint(24, 72)
        rainfall_event[i:i+duration] = 1

# ------------------------
# TURBIDITY MODEL
# ------------------------
turbidity = (
    6
    + 5 * season_cycle
    + 15 * rainfall_event
    + np.random.normal(0, 1.2, HOURS)
)

turbidity = np.clip(turbidity, 1, None)

# ------------------------
# RAW FLOW RATE
# ------------------------
daily_cycle = np.sin(2 * np.pi * time / 24)

raw_flow_rate = (
    6000
    + 700 * daily_cycle
    + 900 * rainfall_event
    + np.random.normal(0, 150, HOURS)
)

# ------------------------
# INFLOW PRESSURE
# ------------------------
inflow_pressure = 5 - 0.0003 * raw_flow_rate + np.random.normal(0, 0.05, HOURS)

# ------------------------
# SENSOR NOISE
# ------------------------
sensor_noise_flag = np.zeros(HOURS)
noise_indices = np.random.choice(HOURS, int(HOURS * 0.02), replace=False)
sensor_noise_flag[noise_indices] = 1

turbidity[noise_indices] *= np.random.uniform(1.1, 1.4, len(noise_indices))

# ------------------------
# SEASON INDEX
# ------------------------
month = timestamps.month

season_index = pd.cut(
    month,
    bins=[0,3,6,9,12],
    labels=[1,2,3,4]
).astype(int)

# ------------------------
# PAC DOSE MODEL
# ------------------------
# PAC dosing proportional to turbidity

pac_dose_ppm = 2.5 * turbidity + np.random.normal(0, 0.8, HOURS)
pac_dose_ppm = np.clip(pac_dose_ppm, 1, None)

# Convert ppm to kg/L (approx)
pac_dose_kgL = pac_dose_ppm / 1e6

# ------------------------
# COAGULATION MODEL
# ------------------------
k = 0.32

outlet_turbidity = turbidity * np.exp(-k * pac_dose_ppm)

# ------------------------
# FILTRATION
# ------------------------
treated_turbidity = outlet_turbidity * np.exp(-0.25)

# ------------------------
# DATAFRAME
# ------------------------
data = pd.DataFrame({

    "timestamp": timestamps,
    "turbidity": turbidity,
    "temperature": temperature,
    "raw_flow_rate": raw_flow_rate,
    "inflow_pressure": inflow_pressure,
    "season_index": season_index,
    "rainfall_event": rainfall_event,
    "sensor_noise_flag": sensor_noise_flag,

    "pac_dose_ppm": pac_dose_ppm,
    "pac_dose_kgL": pac_dose_kgL,

    "outlet_turbidity": outlet_turbidity,
    "treated_turbidity": treated_turbidity
})

# ------------------------
# EXPORT
# ------------------------
data.to_csv("data/synthetic_raw_water.csv", index=False)

print("Synthetic dataset with PAC dosing generated successfully.")
print("Rows:", len(data))