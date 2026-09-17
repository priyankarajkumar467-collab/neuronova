# WatchWise AI
## Intelligent OTT Audience Segmentation & Personalization

---

## 1. Project Overview

WatchWise AI is a containerized machine learning service designed for OTT audience segmentation and personalized content recommendations.

The system analyzes viewer behavior such as:

- Watch time
- Average session duration
- Session frequency
- Weekend viewing behavior
- Completion rate
- Top content genres

An unsupervised clustering model identifies behavioral audience segments. The trained model is persisted and exposed through a REST API.

The system also provides transparent rule-based recommendations based on viewer behavior.

---

## 2. Problem Statement

OTT platforms serve users with different viewing patterns.

Traditional recommendation approaches may not clearly explain why a viewer belongs to a particular audience group.

WatchWise AI addresses this by:

1. Preparing viewer activity data.
2. Extracting behavioral features.
3. Standardizing numerical and categorical-derived features.
4. Applying unsupervised clustering.
5. Selecting the number of clusters using clustering evidence.
6. Persisting the preprocessing and trained model.
7. Providing predictions through a REST API.
8. Generating transparent recommendations.
9. Evaluating segmentation quality automatically.
10. Packaging the complete system using Docker Compose.

---

## 3. Dataset

No official viewer activity CSV was supplied with the problem statement.

Therefore, WatchWise AI uses a synthetic OTT viewer activity dataset generated specifically for this prototype.

The dataset contains 1,200 simulated viewers.

The synthetic data generator creates realistic behavioral variation using latent behavioral profiles such as:

- Deep viewers
- Casual viewers
- Explorer viewers
- Weekend viewers

These profiles are used only during synthetic data generation.

They are NOT included as labels in the clustering dataset.

Therefore, the actual segmentation process remains unsupervised.

### Dataset Columns

| Feature | Description |
|---|---|
| user_id | Unique viewer identifier |
| watch_time_hours | Total viewing time |
| avg_session_mins | Average viewing session duration |
| session_count | Number of viewing sessions |
| top_genres | Viewer-preferred genres |
| weekend_ratio | Proportion of viewing during weekends |
| completion_rate | Percentage of content completed |

---

## 4. Feature Engineering

The following behavioral features are used by the machine learning model:

### Numerical Features

- watch_time_hours
- avg_session_mins
- session_count
- weekend_ratio
- completion_rate

### Genre Features

The top genre information is converted into binary features:

- genre_action
- genre_comedy
- genre_drama
- genre_thriller
- genre_romance
- genre_sci-fi
- genre_animation
- genre_documentary

A value of 1 indicates that the genre is present in the viewer's top genres.

A value of 0 indicates that it is not present.

---

## 5. Machine Learning Approach

WatchWise AI uses unsupervised clustering.

The pipeline consists of:

```text
Viewer Activity Data
        ↓
Feature Engineering
        ↓
StandardScaler
        ↓
KMeans Clustering
        ↓
Audience Segment