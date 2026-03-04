# models/physics_model.py

import numpy as np


def coagulation(turbidity, pac_dose_ppm):
    """
    PAC coagulation removal model
    """

    k = 0.12  # stronger realistic removal

    outlet_turbidity = turbidity * np.exp(-k * pac_dose_ppm)

    return outlet_turbidity


def filtration(outlet_turbidity):
    """
    Rapid sand filtration polishing
    """

    kf = 0.45

    treated_turbidity = outlet_turbidity * np.exp(-kf)

    return treated_turbidity


def run_treatment(state):

    turbidity = state["turbidity"]
    pac_dose_ppm = state["pac_dose_ppm"]

    outlet = coagulation(turbidity, pac_dose_ppm)

    treated = filtration(outlet)

    return {
        "outlet_turbidity": outlet,
        "treated_turbidity": treated
    }