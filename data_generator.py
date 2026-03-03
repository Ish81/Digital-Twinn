# import numpy as np
# import pandas as pd

# # ------------------------
# # CONFIG
# # ------------------------
# HOURS = 8640
# START_DATE = "2024-01-01"
# np.random.seed(42)

# # ------------------------
# # TIME
# # ------------------------
# timestamps = pd.date_range(start=START_DATE, periods=HOURS, freq="H")
# time = np.arange(HOURS)

# # Seasonal + daily cycles
# season_cycle = np.sin(2 * np.pi * time / (24 * 180))
# daily_cycle = np.sin(2 * np.pi * time / 24)

# # ------------------------
# # Rainfall events (clustered)
# # ------------------------
# rainfall_event = np.zeros(HOURS)

# for i in range(0, HOURS, 500):
#     if np.random.rand() > 0.65:
#         duration = np.random.randint(12, 48)
#         rainfall_event[i:i+duration] = 1

# # ------------------------
# # Flow rate (linked to rainfall)
# # ------------------------
# raw_flow_rate = (
#     6000
#     + 600 * daily_cycle
#     + 1000 * season_cycle
#     + 800 * rainfall_event
#     + np.random.normal(0, 120, HOURS)
# )

# # ------------------------
# # Pressure (inverse to flow)
# # ------------------------
# inflow_pressure = 5 - 0.0003 * raw_flow_rate + np.random.normal(0, 0.05, HOURS)

# # ------------------------
# # Turbidity (rain driven)
# # ------------------------
# turbidity = (
#     4
#     + 7 * rainfall_event
#     + 0.002 * raw_flow_rate
#     + np.random.normal(0, 0.4, HOURS)
# )

# # ------------------------
# # Organic load (linked to turbidity)
# # ------------------------
# organic_load = (
#     25
#     + 2.5 * turbidity
#     + 4 * rainfall_event
#     + np.random.normal(0, 1.5, HOURS)
# )

# # ------------------------
# # Temperature (seasonal)
# # ------------------------
# temperature = 25 + 5 * season_cycle + np.random.normal(0, 0.4, HOURS)

# # ------------------------
# # Alkalinity
# # ------------------------
# alkalinity = 110 + 10 * season_cycle + np.random.normal(0, 4, HOURS)

# # ------------------------
# # pH (buffered by alkalinity)
# # ------------------------
# pH = 7.1 + 0.002 * alkalinity - 0.04 * rainfall_event + np.random.normal(0, 0.04, HOURS)

# # ------------------------
# # Hardness (slow seasonal drift)
# # ------------------------
# hardness = 160 + 15 * season_cycle + np.random.normal(0, 4, HOURS)

# # ------------------------
# # TDS
# # ------------------------
# tds = 320 + 35 * season_cycle + 3 * rainfall_event + np.random.normal(0, 8, HOURS)

# # ------------------------
# # Conductivity (correlated with TDS)
# # ------------------------
# conductivity = tds * 1.6 + np.random.normal(0, 4, HOURS)

# # ------------------------
# # Sensor noise flag
# # ------------------------
# sensor_noise_flag = np.zeros(HOURS)
# noise_indices = np.random.choice(HOURS, int(HOURS * 0.02), replace=False)
# sensor_noise_flag[noise_indices] = 1

# # Inject sensor anomalies
# turbidity[noise_indices] *= np.random.uniform(1.2, 1.7, len(noise_indices))
# pH[noise_indices] += np.random.uniform(-0.25, 0.25, len(noise_indices))

# # ------------------------
# # Season Index (1-4)
# # ------------------------
# month = timestamps.month
# season_index = pd.cut(
#     month,
#     bins=[0, 3, 6, 9, 12],
#     labels=[1, 2, 3, 4]
# ).astype(int)

# # ------------------------
# # DataFrame
# # ------------------------
# data = pd.DataFrame({
#     "timestamp": timestamps,
#     "turbidity": turbidity,
#     "pH": pH,
#     "hardness": hardness,
#     "alkalinity": alkalinity,
#     "temperature": temperature,
#     "raw_flow_rate": raw_flow_rate,
#     "tds": tds,
#     "conductivity": conductivity,
#     "inflow_pressure": inflow_pressure,
#     "organic_load": organic_load,
#     "season_index": season_index,
#     "rainfall_event": rainfall_event,
#     "sensor_noise_flag": sensor_noise_flag
# })

# # Remove negative values
# numeric_cols = data.columns.drop("timestamp")
# data[numeric_cols] = data[numeric_cols].clip(lower=0)

# # ------------------------
# # Export
# # ------------------------
# data.to_csv("synthetic_water_treatment_8640.csv", index=False)

# print("8640 rows generated successfully.")

import numpy as np
import pandas as pd

# ------------------------
# CONFIG
# ------------------------
HOURS = 8760   # Full year (recommended)
START_DATE = "2024-01-01"
np.random.seed(42)

# ------------------------
# TIME
# ------------------------
timestamps = pd.date_range(start=START_DATE, periods=HOURS, freq="h")
time = np.arange(HOURS)

# ------------------------
# PUNE SEASON INDEX
# ------------------------
def get_season(month):
    if month in [12, 1, 2]:
        return 1  # Winter
    elif month in [3, 4, 5]:
        return 2  # Summer
    elif month in [6, 7, 8, 9]:
        return 3  # Monsoon
    else:
        return 4  # Post-Monsoon

season_index = np.array([get_season(m) for m in timestamps.month])

# ------------------------
# Seasonal & Daily Cycles
# ------------------------
yearly_cycle = np.sin(2 * np.pi * time / (24 * 365))
daily_cycle = np.sin(2 * np.pi * time / 24)

# ------------------------
# Rainfall Events (Pune Monsoon Heavy)
# ------------------------
rainfall_event = np.zeros(HOURS)

for i in range(HOURS):
    if season_index[i] == 3:  # Monsoon
        if np.random.rand() < 0.30:
            rainfall_event[i] = 1
    else:
        if np.random.rand() < 0.03:
            rainfall_event[i] = 1

# Create clustered rainfall bursts
for i in range(0, HOURS, 200):
    if rainfall_event[i] == 1:
        duration = np.random.randint(6, 36)
        rainfall_event[i:i+duration] = 1

# ------------------------
# Raw Flow Rate
# ------------------------
raw_flow_rate = (
    5800
    + 500 * daily_cycle
    + 900 * yearly_cycle
    + 1000 * rainfall_event
    + np.random.normal(0, 120, HOURS)
)

# ------------------------
# Pressure (Inverse relation)
# ------------------------
inflow_pressure = 5 - 0.00035 * raw_flow_rate + np.random.normal(0, 0.05, HOURS)

# ------------------------
# Turbidity (Rain driven + decay)
# ------------------------
turbidity = np.zeros(HOURS)

for i in range(HOURS):
    base = 3 + 0.002 * raw_flow_rate[i]
    rain_effect = 8 if rainfall_event[i] == 1 else 0
    
    # decay effect after rainfall
    if i > 0 and rainfall_event[i-1] == 1:
        rain_effect *= 0.7
        
    turbidity[i] = base + rain_effect + np.random.normal(0, 0.4)

# ------------------------
# Organic Load
# ------------------------
organic_load = (
    20
    + 2.5 * turbidity
    + 3 * rainfall_event
    + np.random.normal(0, 1.5, HOURS)
)

# ------------------------
# Temperature (Pune Specific)
# ------------------------
temperature = (
    26
    + 6 * yearly_cycle
    + 2 * (season_index == 2)   # hotter summer
    + np.random.normal(0, 0.5, HOURS)
)

# ------------------------
# Alkalinity
# ------------------------
alkalinity = 105 + 12 * yearly_cycle - 4 * rainfall_event + np.random.normal(0, 4, HOURS)

# ------------------------
# pH
# ------------------------
pH = 7.0 + 0.002 * alkalinity - 0.05 * rainfall_event + np.random.normal(0, 0.04, HOURS)

# ------------------------
# Hardness
# ------------------------
hardness = 150 + 18 * yearly_cycle + np.random.normal(0, 4, HOURS)

# ------------------------
# TDS
# ------------------------
tds = 300 + 40 * yearly_cycle + 4 * rainfall_event + np.random.normal(0, 8, HOURS)

# ------------------------
# Conductivity
# ------------------------
conductivity = tds * 1.6 + np.random.normal(0, 4, HOURS)

# ------------------------
# Sensor Noise (2%)
# ------------------------
sensor_noise_flag = np.zeros(HOURS)
noise_indices = np.random.choice(HOURS, int(HOURS * 0.02), replace=False)
sensor_noise_flag[noise_indices] = 1

turbidity[noise_indices] *= np.random.uniform(1.3, 1.8, len(noise_indices))
pH[noise_indices] += np.random.uniform(-0.3, 0.3, len(noise_indices))

# ------------------------
# Create DataFrame
# ------------------------
data = pd.DataFrame({
    "timestamp": timestamps,
    "turbidity": turbidity,
    "pH": pH,
    "hardness": hardness,
    "alkalinity": alkalinity,
    "temperature": temperature,
    "raw_flow_rate": raw_flow_rate,
    "tds": tds,
    "conductivity": conductivity,
    "inflow_pressure": inflow_pressure,
    "organic_load": organic_load,
    "season_index": season_index,
    "rainfall_event": rainfall_event,
    "sensor_noise_flag": sensor_noise_flag
})

# Remove negative values
numeric_cols = data.columns.drop("timestamp")
data[numeric_cols] = data[numeric_cols].clip(lower=0)

# ------------------------
# Export
# ------------------------
data.to_csv("synthetic_water_treatment_pune_8760.csv", index=False)

print("8760 Pune-realistic rows generated successfully.")