import pandas as pd
import numpy as np


def get_default_df():

    df = pd.read_csv("data/nfl.csv")

    # Grab dummy variables
    dummy_vars = pd.get_dummies(df[["opp", "team"]])

    # Add our dummy columns into the features df
    df[list(dummy_vars.columns)] = dummy_vars

    # Define the features
    feature_df = df.drop(["result", "date", "opp", "team", "margin",
                          "points", "points_allowed", "total_points"], axis=1)

    # Grab column names
    columns = list(feature_df.columns)

    zeros = np.zeros(shape=(1, 82))

    default_df = pd.DataFrame(zeros, columns=columns)

    return default_df


def get_form_data():
    features = ["Team", "Opponent", "Third", "Third Allowed", "TOP", "First Downs",
                "First Downs Allowed", "Home or Away", "Pass Yards", "Pass Yards Allowed",
                "Penalty Yards", "Plays", "Rush Yards", "Rush Yards Allowed", "Sacked", "Sacks",
                "Takeaways", "Total Yards", "Total Yards Allowed", "Turnovers"]

    form_names = ["team", "opp", "third_per", "third_per_allowed", "TOP", "first_downs",
                  "first_downs_allowed", "ha", "pass_yards", "pass_yards_allowed", "penalty_yards",
                  "plays", "rush_yards", "rush_yards_allowed", "sacked", "sacks", "takeaways",
                  "total_yards", "total_yards_allowed", "turnovers"]

    placeholders = ["team", "opponent", "third", "third-allowed", "top", "first-downs",
                    "first-downs-allowed", "ha", "pass-yards", "pass-yards-allowed", "penalty-yards",
                    "plays", "rush-yards", "rush-yards-allowed", "sacked", "sacks", "takeaways",
                    "total-yards", "total-yards-allowed", "turnovers"]

    form_df = pd.DataFrame({
        "feature": features,
        "form_name": form_names,
        "placeholder": placeholders
    })

    form_data = form_df.to_dict(orient="records")

    return form_data, form_names
