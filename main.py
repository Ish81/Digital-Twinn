# main.py

import pandas as pd
from models.physics_model import run_treatment
from optimization.cost_model import compute_cost
from utils.config import TURBIDITY_LIMIT
from simulation.scenarios import rainfall_spike

data = pd.read_csv("data/synthetic_raw_water.csv")

# Strong rainfall disturbance
data = rainfall_spike(data, start_index=2000, duration=48)

results = []
previous_dose = 5
filter_age = 1
max_ramp = 3      # max change per hour
max_dose = 25

for _, row in data.iterrows():

    state = {
        "turbidity": row["turbidity"],
        "pH": row["pH"],
        "raw_flow_rate": row["raw_flow_rate"]
    }

    # Controller target
    target_dose = 0.8 * state["turbidity"]

    # Ramp limit (real actuator constraint)
    delta = target_dose - previous_dose
    if delta > max_ramp:
        delta = max_ramp
    if delta < -max_ramp:
        delta = -max_ramp

    dose = previous_dose + delta
    dose = min(dose, max_dose)
    dose = max(dose, 0)

    treatment = run_treatment(state, dose, filter_age)

    cost_info = compute_cost(
        state["raw_flow_rate"],
        dose,
        treatment["treated_turbidity"]
    )

    compliant = 1 if treatment["treated_turbidity"] <= TURBIDITY_LIMIT else 0
    reward = -cost_info["total_cost"]

    results.append({
        "dose": dose,
        "treated_turbidity": treatment["treated_turbidity"],
        "total_cost": cost_info["total_cost"],
        "compliant": compliant,
        "reward": reward
    })

    previous_dose = dose
    filter_age += 0.01

results_df = pd.DataFrame(results)
data = pd.concat([data, results_df], axis=1)

data.to_csv("data/full_simulation_output.csv", index=False)

compliance_rate = data["compliant"].mean() * 100
avg_cost = data["total_cost"].mean()
avg_turbidity = data["treated_turbidity"].mean()

print("\nFull Digital Twin Simulation Completed.")
print(f"Compliance Rate: {compliance_rate:.2f}%")
print(f"Average Cost: {avg_cost:.2f}")
print(f"Average Treated Turbidity: {avg_turbidity:.2f}")