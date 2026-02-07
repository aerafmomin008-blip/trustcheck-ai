import pandas as pd
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score
import joblib

# Load dataset
df = pd.read_csv("data/websites.csv")

# Features & label
X = df[
    [
        "domain_age_days",
        "ssl_valid",
        "whois_private",
        "reputation_score",
        "malware_flag",
        "phishing_flag"
    ]
]

y = df["label"]

# Train-test split
X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.25, random_state=42
)

# Model
model = RandomForestClassifier(
    n_estimators=100,
    random_state=42
)

model.fit(X_train, y_train)

# Accuracy
preds = model.predict(X_test)
accuracy = accuracy_score(y_test, preds)
print("Model accuracy:", accuracy)

# Save model
joblib.dump(model, "model/trust_model.pkl")
