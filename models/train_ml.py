# models/train_ml.py

import os
import joblib
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_squared_error, mean_absolute_error, r2_score

from sklearn.linear_model import LinearRegression
from sklearn.tree import DecisionTreeRegressor
from sklearn.ensemble import RandomForestRegressor


# =====================================================
# CONFIG
# =====================================================

DATA_PATH = "data/synthetic_raw_water_new.csv"

RESULT_DIR = "models/results"
MODEL_DIR = "models/saved_models"

os.makedirs(RESULT_DIR, exist_ok=True)
os.makedirs(MODEL_DIR, exist_ok=True)


# =====================================================
# LOAD DATA
# =====================================================

data = pd.read_csv(DATA_PATH)

print("\nDataset Loaded Successfully")
print("Shape:", data.shape)


# =====================================================
# FEATURES / TARGETS
# =====================================================

# -------- Task A: Predict PAC Dose --------
X_pac = data[
    [
        "turbidity",
        "temperature",
        "raw_flow_rate",
        "inflow_pressure",
        "season_index",
        "rainfall_event",
        "sensor_noise_flag"
    ]
]

y_pac = data["pac_dose_ppm"]


# -------- Task B: Predict Treated Turbidity --------
X_treat = data[
    [
        "turbidity",
        "temperature",
        "raw_flow_rate",
        "inflow_pressure",
        "season_index",
        "rainfall_event",
        "sensor_noise_flag",
        "pac_dose_ppm"
    ]
]

y_treat = data["treated_turbidity"]


# =====================================================
# TRAIN / TEST SPLIT
# =====================================================

X_train_pac, X_test_pac, y_train_pac, y_test_pac = train_test_split(
    X_pac, y_pac, test_size=0.2, random_state=42
)

X_train_t, X_test_t, y_train_t, y_test_t = train_test_split(
    X_treat, y_treat, test_size=0.2, random_state=42
)


# =====================================================
# MODELS
# =====================================================

models = {
    "Linear Regression": LinearRegression(),
    "Decision Tree": DecisionTreeRegressor(
        max_depth=12,
        random_state=42
    ),
    "Random Forest": RandomForestRegressor(
        n_estimators=200,
        max_depth=15,
        random_state=42,
        n_jobs=-1
    )
}


# =====================================================
# EVALUATION FUNCTION
# =====================================================

def evaluate_model(name, model, X_train, X_test, y_train, y_test):

    model.fit(X_train, y_train)

    pred_train = model.predict(X_train)
    pred_test = model.predict(X_test)

    rmse = np.sqrt(mean_squared_error(y_test, pred_test))
    mae = mean_absolute_error(y_test, pred_test)
    r2 = r2_score(y_test, pred_test)

    train_r2 = r2_score(y_train, pred_train)
    test_r2 = r2_score(y_test, pred_test)

    return {
        "Model": name,
        "RMSE": rmse,
        "MAE": mae,
        "R2": r2,
        "Train_R2": train_r2,
        "Test_R2": test_r2,
        "model_obj": model
    }


# =====================================================
# TASK A: PAC DOSE PREDICTION
# =====================================================

print("\n==============================")
print("TASK A : PAC DOSE PREDICTION")
print("==============================")

results_pac = []

for name, model in models.items():

    res = evaluate_model(
        name,
        model,
        X_train_pac,
        X_test_pac,
        y_train_pac,
        y_test_pac
    )

    results_pac.append(res)

pac_df = pd.DataFrame(results_pac).drop(columns=["model_obj"])
print("\nPAC Dose Results:\n")
print(pac_df)


# =====================================================
# BEST MODEL PAC
# =====================================================

best_pac_idx = pac_df["R2"].idxmax()
best_pac_name = pac_df.loc[best_pac_idx, "Model"]
best_pac_model = results_pac[best_pac_idx]["model_obj"]

joblib.dump(
    best_pac_model,
    f"{MODEL_DIR}/best_pac_model.pkl"
)

print(f"\nBest PAC Model Saved: {best_pac_name}")


# =====================================================
# FEATURE IMPORTANCE PAC
# =====================================================

if hasattr(best_pac_model, "feature_importances_"):

    imp = best_pac_model.feature_importances_

    plt.figure(figsize=(8, 5))
    plt.bar(X_pac.columns, imp)
    plt.xticks(rotation=45)
    plt.title("Feature Importance - PAC Dose Model")
    plt.tight_layout()
    plt.savefig(f"{RESULT_DIR}/pac_feature_importance.png")
    plt.show()


# =====================================================
# TASK B: TREATED TURBIDITY PREDICTION
# =====================================================

print("\n===================================")
print("TASK B : TREATED TURBIDITY PREDICTION")
print("===================================")

results_t = []

for name, model in models.items():

    res = evaluate_model(
        name,
        model,
        X_train_t,
        X_test_t,
        y_train_t,
        y_test_t
    )

    results_t.append(res)

treat_df = pd.DataFrame(results_t).drop(columns=["model_obj"])
print("\nTreated Turbidity Results:\n")
print(treat_df)


# =====================================================
# BEST MODEL TREATMENT
# =====================================================

best_t_idx = treat_df["R2"].idxmax()
best_t_name = treat_df.loc[best_t_idx, "Model"]
best_t_model = results_t[best_t_idx]["model_obj"]

joblib.dump(
    best_t_model,
    f"{MODEL_DIR}/best_treatment_model.pkl"
)

print(f"\nBest Treatment Model Saved: {best_t_name}")


# =====================================================
# FEATURE IMPORTANCE TREATMENT
# =====================================================

if hasattr(best_t_model, "feature_importances_"):

    imp = best_t_model.feature_importances_

    plt.figure(figsize=(8, 5))
    plt.bar(X_treat.columns, imp)
    plt.xticks(rotation=45)
    plt.title("Feature Importance - Treated Turbidity Model")
    plt.tight_layout()
    plt.savefig(f"{RESULT_DIR}/treatment_feature_importance.png")
    plt.show()


# =====================================================
# SAVE RESULT TABLES
# =====================================================

pac_df.to_csv(f"{RESULT_DIR}/pac_results.csv", index=False)
treat_df.to_csv(f"{RESULT_DIR}/treatment_results.csv", index=False)

print("\nAll Results Saved Successfully.")
