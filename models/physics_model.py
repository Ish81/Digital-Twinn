# models/physics_model.py

import numpy as np
from utils.config import TANK_VOLUME, TANK_DEPTH

def coagulation(turbidity, dose, pH):

    k = 0.33 - 0.02 * abs(pH - 7)
    k = max(k, 0.20)

    effective_dose = dose / (1 + 0.03 * dose)

    return turbidity * np.exp(-k * effective_dose)


def sedimentation(turbidity, flow_rate):

    retention_time = TANK_VOLUME / flow_rate
    vs = 1.4

    # Overload effect when turbidity very high
    overload_factor = 1
    if turbidity > 60:
        overload_factor = 0.6  # sludge carryover reduces efficiency

    return turbidity * np.exp(-vs * retention_time / TANK_DEPTH) / overload_factor


def filtration(turbidity, filter_age):

    clogging_factor = 1 + 0.02 * filter_age

    # Breakthrough if turbidity too high
    if turbidity > 30:
        breakthrough = 1.5
    else:
        breakthrough = 1

    return turbidity * np.exp(-0.22 / clogging_factor) * breakthrough


def run_treatment(raw_state, dose, filter_age=1):

    t1 = coagulation(raw_state["turbidity"], dose, raw_state["pH"])
    t2 = sedimentation(t1, raw_state["raw_flow_rate"])
    t3 = filtration(t2, filter_age)

    return {
        "treated_turbidity": max(t3, 0),
        "retention_time": TANK_VOLUME / raw_state["raw_flow_rate"]
    }