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

    # Make row of all zeros
    zeros = np.zeros(shape=(1, 82))

    default_df = pd.DataFrame(zeros, columns=columns)

    return default_df


form_names = ["team", "opp", "third_per", "third_per_allowed", "TOP", "first_downs",
              "first_downs_allowed", "ha", "pass_yards", "pass_yards_allowed", "penalty_yards",
              "plays", "rush_yards", "rush_yards_allowed", "sacked", "sacks", "takeaways",
              "total_yards", "total_yards_allowed", "turnovers"]

teams_abbrev = {
    "ARI": "Arizona Cardinals",
    "ATL": "Atlanta Falcons",
    "BAL": "Baltimore Ravens",
    "BUF": "Buffalo Bills",
    "CAR": "Carolina Panthers",
    "CHI": "Chicago Bears",
    "CIN": "Cincinnati Bengals",
    "CLE": "Cleveland Browns",
    "DAL": "Dallas Cowboys",
    "DEN": "Denver Broncos",
    "DET": "Detroit Lions",
    "GB": "Green Bay Packers",
    "HOU": "Houston Texans",
    "IND": "Indianapolis Colts",
    "JAX": "Jacksonville Jaguars",
    "KC": "Kansas City Chiefs",
    "LAC": "Los Angeles Chargers",
    "LAR": "Los Angeles Rams",
    "MIA": "Miami Dolphins",
    "MIN": "Minnesota Vikings",
    "NE": "New England Patriots",
    "NO": "New Orleans Saints",
    "NYG": "New York Giants",
    "NYJ": "New York Jets",
    "OAK": "Oakland Raiders",
    "PHI": "Philadelphia Eagles",
    "PIT": "Pittsburgh Steelers",
    "SEA": "San Francisco 49ers",
    "SF": "Seattle Seahawks",
    "TB": "Tampa Bay Buccaneers",
    "TEN": "Tennessee Titans",
    "WAS": "Washington Redskins"
}
