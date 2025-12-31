import pandas as pd
import numpy as np
import joblib
import os

from sklearn.linear_model import LinearRegression
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import mean_absolute_error

# Load data
df = pd.read_csv("data/prices.csv")

X = df[["day"]]
y = df["price"]

models = {
    "LinearRegression": LinearRegression(),
    "RandomForest": RandomForestRegressor(n_estimators=100, random_state=42)
}

best_model = None
best_error = float("inf")

for name, model in models.items():
    model.fit(X, y)
    preds = model.predict(X)
    error = mean_absolute_error(y, preds)
    print(f"{name} MAE: {error:.2f}")

    if error < best_error:
        best_error = error
        best_model = model

os.makedirs("model", exist_ok=True)
joblib.dump(best_model, "model/price_model.pkl")

print("✅ Best model saved")
