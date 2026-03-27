# models/physics_model.py

import numpy as np

def coagulation(turbidity, pac_dose_ppm):

    base_k = 0.12

    if turbidity <= 25:
        k = base_k
    else:
        reduction = 1 - 0.015*(turbidity - 25)
        reduction = max(reduction, 0.5)
        k = base_k * reduction

    effective_dose = pac_dose_ppm / (1 + 0.03 * pac_dose_ppm)

    outlet_turbidity = turbidity * np.exp(-k * effective_dose)

    return outlet_turbidity


def filtration(outlet_turbidity):

    kf = 0.45

    return outlet_turbidity * np.exp(-kf)


def run_treatment(state):

    turbidity = state["turbidity"]
    pac_dose_ppm = state["pac_dose_ppm"]

    outlet = coagulation(turbidity, pac_dose_ppm)
    treated = filtration(outlet)

    return {
        "outlet_turbidity": outlet,
        "treated_turbidity": treated
    }