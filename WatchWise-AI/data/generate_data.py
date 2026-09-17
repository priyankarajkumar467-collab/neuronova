import pandas as pd
import random

random.seed(42)

users = []

genres = [
    "Action",
    "Comedy",
    "Drama",
    "Thriller",
    "Romance",
    "Sci-Fi",
    "Animation",
    "Documentary"
]

for user_id in range(1, 1201):

    profile = random.choice([
        "deep",
        "casual",
        "explorer",
        "weekend"
    ])

    if profile == "deep":
        watch_time = random.uniform(25, 60)
        session = random.uniform(45, 100)
        sessions = random.randint(20, 45)
        weekend = random.uniform(0.20, 0.45)
        completion = random.uniform(0.75, 0.98)
        top_genres = random.sample(genres, 2)

    elif profile == "casual":
        watch_time = random.uniform(3, 15)
        session = random.uniform(10, 30)
        sessions = random.randint(3, 15)
        weekend = random.uniform(0.15, 0.40)
        completion = random.uniform(0.35, 0.70)
        top_genres = random.sample(genres, 2)

    elif profile == "explorer":
        watch_time = random.uniform(15, 35)
        session = random.uniform(25, 55)
        sessions = random.randint(10, 30)
        weekend = random.uniform(0.25, 0.55)
        completion = random.uniform(0.50, 0.80)
        top_genres = random.sample(genres, 4)

    else:
        watch_time = random.uniform(10, 30)
        session = random.uniform(25, 60)
        sessions = random.randint(8, 25)
        weekend = random.uniform(0.65, 0.95)
        completion = random.uniform(0.50, 0.85)
        top_genres = random.sample(genres, 2)

    users.append({
        "user_id": user_id,
        "watch_time_hours": round(watch_time, 2),
        "avg_session_mins": round(session, 2),
        "session_count": sessions,
        "top_genres": ", ".join(top_genres),
        "weekend_ratio": round(weekend, 2),
        "completion_rate": round(completion, 2)
    })


df = pd.DataFrame(users)

df.to_csv("user_activity.csv", index=False)

print("Dataset created successfully!")
print(f"Total users: {len(df)}")
print("File saved as: user_activity.csv")