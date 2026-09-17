import pandas as pd
import json
import os

from sklearn.preprocessing import StandardScaler
from sklearn.cluster import KMeans
from sklearn.metrics import silhouette_score
from sklearn.pipeline import Pipeline


# -----------------------------------------
# 1. Load dataset
# -----------------------------------------

DATA_PATH = "data/user_activity.csv"

df = pd.read_csv(DATA_PATH)

print("Dataset loaded successfully!")
print("Total users:", len(df))


# -----------------------------------------
# 2. Prepare genre features
# -----------------------------------------

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


# -----------------------------------------
# 3. Select ML features
# -----------------------------------------

features = [
    "watch_time_hours",
    "avg_session_mins",
    "session_count",
    "weekend_ratio",
    "completion_rate"
]

features += [f"genre_{genre}" for genre in genres]

X = df[features]


# -----------------------------------------
# 4. Test different cluster counts
# -----------------------------------------

print("\nTesting cluster counts...")

scores = {}

for k in range(2, 7):

    model = Pipeline([
        ("scaler", StandardScaler()),
        ("kmeans", KMeans(
            n_clusters=k,
            random_state=42,
            n_init=10
        ))
    ])

    labels = model.fit_predict(X)

    score = silhouette_score(
        model.named_steps["scaler"].transform(X),
        labels
    )

    scores[k] = score

    print(f"K = {k} | Silhouette Score = {score:.4f}")


# -----------------------------------------
# 5. Select best K
# -----------------------------------------

best_k = max(scores, key=scores.get)

print("\nBest number of segments:", best_k)


# -----------------------------------------
# 6. Train final model
# -----------------------------------------

final_model = Pipeline([
    ("scaler", StandardScaler()),
    ("kmeans", KMeans(
        n_clusters=best_k,
        random_state=42,
        n_init=10
    ))
])

df["segment_id"] = final_model.fit_predict(X)


# -----------------------------------------
# 7. Create models folder
# -----------------------------------------

os.makedirs("models", exist_ok=True)


# -----------------------------------------
# 8. Save model
# -----------------------------------------

import joblib

joblib.dump(
    final_model,
    "models/watchwise_model.joblib"
)


# -----------------------------------------
# 9. Create segment information
# -----------------------------------------

segment_info = {}

for segment_id in sorted(df["segment_id"].unique()):

    segment_data = df[df["segment_id"] == segment_id]

    segment_info[str(segment_id)] = {
        "user_count": int(len(segment_data)),
        "avg_watch_time_hours": round(
            segment_data["watch_time_hours"].mean(), 2
        ),
        "avg_session_mins": round(
            segment_data["avg_session_mins"].mean(), 2
        ),
        "avg_session_count": round(
            segment_data["session_count"].mean(), 2
        ),
        "avg_completion_rate": round(
            segment_data["completion_rate"].mean(), 2
        ),
        "avg_weekend_ratio": round(
            segment_data["weekend_ratio"].mean(), 2
        )
    }


# -----------------------------------------
# 10. Save segment information
# -----------------------------------------

with open("models/segments.json", "w") as file:
    json.dump(segment_info, file, indent=4)


# -----------------------------------------
# 11. Training complete
# -----------------------------------------

print("\n================================")
print("WATCHWISE AI TRAINING COMPLETE")
print("================================")

print("Model saved:")
print("models/watchwise_model.joblib")

print("\nSegment information saved:")
print("models/segments.json")

print("\nSegment summary:")

for segment, info in segment_info.items():

    print(
        f"Segment {segment}: "
        f"{info['user_count']} users | "
        f"Watch time: {info['avg_watch_time_hours']} hrs | "
        f"Completion: {info['avg_completion_rate']}"
    )