from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field
import pandas as pd
import joblib
import json


# -----------------------------------------
# FastAPI application
# -----------------------------------------

app = FastAPI(
    title="WatchWise AI",
    description="OTT Audience Segmentation & Personalization API",
    version="1.0"
)


# -----------------------------------------
# CORS
# -----------------------------------------

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# -----------------------------------------
# Load trained model
# -----------------------------------------

model = joblib.load("models/watchwise_model.joblib")


# Load segment information
with open("models/segments.json", "r") as file:
    segments = json.load(file)


# -----------------------------------------
# Request format
# -----------------------------------------

class ViewerData(BaseModel):

    watch_time_hours: float = Field(ge=0)

    avg_session_mins: float = Field(ge=0)

    session_count: int = Field(ge=0)

    weekend_ratio: float = Field(
        ge=0,
        le=1
    )

    completion_rate: float = Field(
        ge=0,
        le=1
    )

    top_genres: str = Field(
        min_length=1
    )


# -----------------------------------------
# Health endpoint
# -----------------------------------------

@app.get("/health")
def health():

    return {
        "status": "healthy",
        "service": "WatchWise AI"
    }


# -----------------------------------------
# Recommendation endpoint
# -----------------------------------------

@app.post("/recommend")
def recommend(viewer: ViewerData):

    # Supported genres
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


    # -----------------------------------------
    # Create viewer feature row
    # -----------------------------------------

    row = {

        "watch_time_hours":
            viewer.watch_time_hours,

        "avg_session_mins":
            viewer.avg_session_mins,

        "session_count":
            viewer.session_count,

        "weekend_ratio":
            viewer.weekend_ratio,

        "completion_rate":
            viewer.completion_rate
    }


    # -----------------------------------------
    # Genre features
    # -----------------------------------------

    for genre in genres:

        row[f"genre_{genre}"] = (

            1
            if genre in viewer.top_genres.lower()
            else 0

        )


    # -----------------------------------------
    # Feature order
    # -----------------------------------------

    features = [

        "watch_time_hours",

        "avg_session_mins",

        "session_count",

        "weekend_ratio",

        "completion_rate"
    ]


    features += [

        f"genre_{genre}"

        for genre in genres
    ]


    # -----------------------------------------
    # Convert to DataFrame
    # -----------------------------------------

    input_data = pd.DataFrame(
        [row]
    )[features]


    # -----------------------------------------
    # Predict segment
    # -----------------------------------------

    segment_id = int(
        model.predict(input_data)[0]
    )


    # -----------------------------------------
    # Get segment profile
    # -----------------------------------------

    segment = segments[
        str(segment_id)
    ]


    # -----------------------------------------
    # Meaningful segment names
    # -----------------------------------------

    segment_names = {

        0: "Casual & Regular Viewers",

        1: "Binge Enthusiasts"
    }


    segment_name = segment_names.get(

        segment_id,

        "General Viewer"
    )


    # -----------------------------------------
    # Transparent recommendation rules
    # -----------------------------------------

    if viewer.watch_time_hours >= 30:

        recommendation = (
            "Long-form movies and "
            "binge-worthy series"
        )

    elif viewer.completion_rate >= 0.80:

        recommendation = (
            "Highly engaging series "
            "with strong story continuity"
        )

    elif viewer.weekend_ratio >= 0.65:

        recommendation = (
            "Weekend entertainment collections "
            "and movie marathons"
        )

    elif len(
        viewer.top_genres.split(",")
    ) >= 3:

        recommendation = (
            "Mixed-genre discovery "
            "and trending content"
        )

    else:

        recommendation = (
            "Popular short-form and "
            "easy-to-watch content"
        )


    # -----------------------------------------
    # Response
    # -----------------------------------------

    return {

        "segment_id":
            segment_id,

        "segment_name":
            segment_name,

        "segment_profile":
            segment,

        "recommendation":
            recommendation
    }