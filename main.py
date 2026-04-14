import pandas as pd
from models.physics_model import run_treatment
from optimization.cost_model import compute_cost
from utils.config import TURBIDITY_LIMIT

# ------------------------
# LOAD DATA
# ------------------------
data = pd.read_csv("data/synthetic_raw_water.csv")

results = []

for _, row in data.iterrows():

    # ------------------------
    # STATE
    # ------------------------
    state = {
        "turbidity": row["turbidity"],
        "pac_dose_ppm": row["pac_dose_ppm"]  # ✅ USE SAME DOSE
    }

    # ------------------------
    # PHYSICS MODEL
    # ------------------------
    treatment = run_treatment(state)

    # ------------------------
    # COST MODEL
    # ------------------------
    cost_info = compute_cost(
        row["raw_flow_rate"],
        row["pac_dose_ppm"],  # ✅ SAME DOSE
        treatment["treated_turbidity"]
    )

    # ------------------------
    # COMPLIANCE
    # ------------------------
    compliant = 1 if treatment["treated_turbidity"] <= TURBIDITY_LIMIT else 0

    results.append({
        "pac_dose_ppm_calc": row["pac_dose_ppm"],
        "outlet_turbidity_calc": treatment["outlet_turbidity"],
        "treated_turbidity_calc": treatment["treated_turbidity"],
        "total_cost": cost_info["total_cost"],
        "compliant": compliant
    })

# ------------------------
# SAVE OUTPUT
# ------------------------
results_df = pd.DataFrame(results)
data = pd.concat([data, results_df], axis=1)

data.to_csv("data/full_simulation_output_new.csv", index=False)

# ------------------------
# METRICS
# ------------------------
compliance_rate = data["compliant"].mean() * 100
avg_cost = data["total_cost"].mean()
avg_turbidity = data["treated_turbidity_calc"].mean()

print("\nFull Digital Twin Simulation Completed.")
print(f"Compliance Rate: {compliance_rate:.2f}%")
print(f"Average Cost: {avg_cost:.2f}")
print(f"Average Treated Turbidity: {avg_turbidity:.2f}")