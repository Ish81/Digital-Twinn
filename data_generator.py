# data_generator.py

import numpy as np
import pandas as pd
import os

HOURS = 8760
START_DATE = "2024-01-01"

np.random.seed(42)

# ------------------------
# TIME
# ------------------------
timestamps = pd.date_range(start=START_DATE, periods=HOURS, freq="h")

# ------------------------
# SEASON FUNCTION (India)
# ------------------------
def get_season(month):
    if month in [12, 1, 2]:
        return 1  # Winter
    elif month in [3, 4, 5]:
        return 2  # Summer
    elif month in [6, 7, 8, 9]:
        return 3  # Monsoon
    else:
        return 4  # Post-monsoon

season_index = np.array([get_season(m) for m in timestamps.month])

# ------------------------
# RAINFALL
# ------------------------
rainfall_event = np.zeros(HOURS)

for i in range(HOURS):
    s = season_index[i]

    if s == 3:
        rainfall_event[i] = np.random.choice([0,1], p=[0.3,0.7])
    elif s == 4:
        rainfall_event[i] = np.random.choice([0,1], p=[0.6,0.4])
    else:
        rainfall_event[i] = 0

# ------------------------
# TURBIDITY (5–50)
# ------------------------
turbidity = np.zeros(HOURS)

for i in range(HOURS):
    s = season_index[i]

    if s in [3,4]:
        turbidity[i] = np.random.uniform(35,50)
    else:
        turbidity[i] = np.random.uniform(5,25)

    if rainfall_event[i] == 1:
        turbidity[i] *= np.random.uniform(1.1,1.3)

turbidity = np.clip(turbidity, 5, 50)

# ------------------------
# TEMPERATURE
# ------------------------
temperature = np.zeros(HOURS)

for i in range(HOURS):
    s = season_index[i]

    if s == 1:
        temperature[i] = np.random.uniform(18,25)
    elif s == 2:
        temperature[i] = np.random.uniform(30,40)
    elif s == 3:
        temperature[i] = np.random.uniform(24,30)
    else:
        temperature[i] = np.random.uniform(20,28)

# ------------------------
# FLOW
# ------------------------
raw_flow_rate = 6000 + 800*rainfall_event + np.random.normal(0,200,HOURS)

# ------------------------
# PRESSURE
# ------------------------
inflow_pressure = 5 - 0.0003*raw_flow_rate + np.random.normal(0,0.05,HOURS)

# ------------------------
# SENSOR NOISE
# ------------------------
sensor_noise_flag = np.zeros(HOURS)
noise_idx = np.random.choice(HOURS, int(HOURS*0.02), replace=False)
sensor_noise_flag[noise_idx] = 1
turbidity[noise_idx] *= np.random.uniform(1.1,1.4,len(noise_idx))

# ------------------------
# PAC DOSE (NONLINEAR)
# ------------------------
a = 1.8
b = 0.04

pac_dose_ppm = a*turbidity + b*(turbidity**2)
pac_dose_ppm += np.random.normal(0,1,HOURS)
pac_dose_ppm = np.clip(pac_dose_ppm, 1, None)

pac_dose_kgL = pac_dose_ppm / 1e6

# ------------------------
# COAGULATION (MATCH MODEL)
# ------------------------
outlet_turbidity = np.zeros(HOURS)

for i in range(HOURS):
    T = turbidity[i]
    dose = pac_dose_ppm[i]

    base_k = 0.12

    if T <= 25:
        k = base_k
    else:
        reduction = 1 - 0.015*(T-25)
        reduction = max(reduction, 0.5)
        k = base_k * reduction

    effective_dose = dose / (1 + 0.03*dose)

    outlet_turbidity[i] = T * np.exp(-k * effective_dose)

# ------------------------
# FILTRATION
# ------------------------
treated_turbidity = outlet_turbidity * np.exp(-0.45)

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
# SAVE
# ------------------------
os.makedirs("data", exist_ok=True)
data.to_csv("data/synthetic_raw_water_new.csv", index=False)

print("Final nonlinear dataset generated.")
print("Rows:", len(data))