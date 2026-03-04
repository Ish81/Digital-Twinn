# main.py

import pandas as pd
import numpy as np
from models.physics_model import run_treatment
from optimization.cost_model import compute_cost
from utils.config import TURBIDITY_LIMIT
from simulation.scenarios import rainfall_spike

# -------------------------
# LOAD DATA
# -------------------------

data = pd.read_csv("data/synthetic_raw_water.csv")

# Inject rainfall disturbance
data = rainfall_spike(data, start_index=2000, duration=48)

results = []

# -------------------------
# SIMULATION LOOP
# -------------------------

for _, row in data.iterrows():

    turbidity = row["turbidity"]

    # PAC dosing rule (coagulation control)
    pac_dose_ppm = 2.8 * turbidity + np.random.normal(0, 1)

    pac_dose_ppm = max(pac_dose_ppm, 1)

    state = {
        "turbidity": turbidity,
        "temperature": row["temperature"],
        "raw_flow_rate": row["raw_flow_rate"],
        "pac_dose_ppm": pac_dose_ppm
    }

    treatment = run_treatment(state)

    cost_info = compute_cost(
        row["raw_flow_rate"],
        pac_dose_ppm,
        treatment["treated_turbidity"]
    )

    compliant = 1 if treatment["treated_turbidity"] <= TURBIDITY_LIMIT else 0

    results.append({
        "pac_dose_ppm_calc": pac_dose_ppm,
        "outlet_turbidity_calc": treatment["outlet_turbidity"],
        "treated_turbidity_calc": treatment["treated_turbidity"],
        "energy": cost_info["energy"],
        "total_cost": cost_info["total_cost"],
        "compliant": compliant
    })

# -------------------------
# SAVE OUTPUT
# -------------------------

results_df = pd.DataFrame(results)

data = pd.concat([data, results_df], axis=1)

data.to_csv("data/full_simulation_output.csv", index=False)

# -------------------------
# METRICS
# -------------------------

compliance_rate = data["compliant"].mean() * 100
avg_cost = data["total_cost"].mean()
avg_turbidity = data["treated_turbidity_calc"].mean()

print("\nFull Digital Twin Simulation Completed.")
print(f"Compliance Rate: {compliance_rate:.2f}%")
print(f"Average Cost: {avg_cost:.2f}")
print(f"Average Treated Turbidity: {avg_turbidity:.2f}")