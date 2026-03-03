# optimization/cost_model.py

from utils.config import (
    CHEMICAL_COST_PER_UNIT,
    ENERGY_COST_PER_KWH,
    TURBIDITY_LIMIT,
    WATER_DENSITY,
    GRAVITY
)

def compute_energy(flow_rate, head=10, efficiency=0.8):
    power = (WATER_DENSITY * GRAVITY * flow_rate * head) / efficiency
    return power / 1000


def compute_cost(flow_rate, dose, treated_turbidity):

    energy = compute_energy(flow_rate)

    chemical_cost = CHEMICAL_COST_PER_UNIT * dose
    energy_cost = ENERGY_COST_PER_KWH * energy

    compliance_penalty = 0
    if treated_turbidity > TURBIDITY_LIMIT:
        compliance_penalty = 180

    overdose_penalty = 0
    if dose > 20:
        overdose_penalty = (dose - 20) * 20

    total_cost = (
        chemical_cost
        + energy_cost
        + compliance_penalty
        + overdose_penalty
    )

    return {
        "energy": energy,
        "total_cost": total_cost,
        "penalty": compliance_penalty,
        "overdose_penalty": overdose_penalty
    }