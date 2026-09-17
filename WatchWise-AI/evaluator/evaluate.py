import pandas as pd
import joblib
import json
import os

from sklearn.metrics import silhouette_score


# Load dataset
df = pd.read_csv("data/user_activity.csv")

# Load trained model
model = joblib.load("models/watchwise_model.joblib")


# Prepare genre features
genres = [
    "action",
    "comedy",
    "drama",
    "thriller",
    "romance",
    "sci-fi",
    "animation",
    "documentary"
]

for genre in genres:
    df[f"genre_{genre}"] = df["top_genres"].apply(
        lambda x: 1 if genre in x.lower() else 0
    )


# Same features used during training
features = [
    "watch_time_hours",
    "avg_session_mins",
    "session_count",
    "weekend_ratio",
    "completion_rate"
]

features += [f"genre_{genre}" for genre in genres]

X = df[features]


# Predict segments
labels = model.predict(X)


# Calculate silhouette score
X_scaled = model.named_steps["scaler"].transform(X)

silhouette = silhouette_score(
    X_scaled,
    labels
)


# Segment distribution
segment_counts = pd.Series(labels).value_counts().sort_index()

distribution = {
    str(segment): int(count)
    for segment, count in segment_counts.items()
}


# Save evaluation results
os.makedirs("evaluator", exist_ok=True)

metrics = {
    "dataset_users": len(df),
    "number_of_segments": len(set(labels)),
    "silhouette_score": round(float(silhouette), 4),
    "segment_distribution": distribution
}


with open("evaluator/metrics.json", "w") as file:
    json.dump(metrics, file, indent=4)


print("================================")
print("WATCHWISE AI EVALUATION COMPLETE")
print("================================")

print("Silhouette Score:", round(float(silhouette), 4))
print("Segments:", len(set(labels)))
print("Metrics saved to: evaluator/metrics.json")