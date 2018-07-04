import pandas as pd
import numpy as np
from keras.models import load_model
from keras import backend
from statsmodels.iolib.smpickle import load_pickle


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
              "first_downs_allowed", "pass_yards", "pass_yards_allowed", "penalty_yards",
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
    "GBP": "Green Bay Packers",
    "HOU": "Houston Texans",
    "IND": "Indianapolis Colts",
    "JAX": "Jacksonville Jaguars",
    "KCC": "Kansas City Chiefs",
    "LAC": "Los Angeles Chargers",
    "LAR": "Los Angeles Rams",
    "MIA": "Miami Dolphins",
    "MIN": "Minnesota Vikings",
    "NEP": "New England Patriots",
    "NOS": "New Orleans Saints",
    "NYG": "New York Giants",
    "NYJ": "New York Jets",
    "OAK": "Oakland Raiders",
    "PHI": "Philadelphia Eagles",
    "PIT": "Pittsburgh Steelers",
    "SFO": "San Francisco 49ers",
    "SEA": "Seattle Seahawks",
    "TBB": "Tampa Bay Buccaneers",
    "TEN": "Tennessee Titans",
    "WAS": "Washington Redskins"
}


def run_win_loss_model(model_input_df, team, opponent):
    deep_model = load_model("models/deep_neural_model_trained.h5")

    encoded_prediction = deep_model.predict_classes(model_input_df)

    data = {}

    if encoded_prediction[0] == 0:
        for key, value in teams_abbrev.items():
            if key == opponent:
                data["winner"] = value
            elif key == team:
                data["loser"] = value
    elif encoded_prediction[0] == 2:
        for key, value in teams_abbrev.items():
            if key == team:
                data["winner"] = value
            elif key == opponent:
                data["loser"] = value

    # Clear the model session
    backend.clear_session()

    return data


def predict_margins(nfl):

    margin_res = load_pickle("models/margin_res.pickle")

    margin_ari_score = 0
    margin_ari_opp = 0
    margins = []

    for key, row in nfl.iterrows():
        if row.team == "ARI":
            team_coeff = margin_ari_score
        else:
            res_team = "team[T." + row.team + "]"
            team_coeff = margin_res.params[res_team]
        if row.opp == "ARI":
            opp_coeff = margin_ari_opp
        else:
            res_opp = "team[T." + row.opp + "]"
            opp_coeff = margin_res.params[res_opp]
        if row.ha == "away":
            ha_coeff = margin_res.params["ha[T.home]"]*-1
        else:
            ha_coeff = margin_res.params["ha[T.home]"]*1

        margin_predict = margin_res.params.Intercept + margin_res.params.third_per*row['third_per'] + \
            margin_res.params.third_per_allowed*row['third_per_allowed'] + margin_res.params.TOP*row['TOP'] + \
            margin_res.params.first_downs * row['first_downs'] + margin_res.params.first_downs_allowed * \
            row['first_downs_allowed'] + margin_res.params.pass_yards*row['pass_yards'] + \
            margin_res.params.pass_yards_allowed*row['pass_yards_allowed'] + margin_res.params.penalty_yards * \
            row['penalty_yards'] + margin_res.params.plays*row['plays'] + margin_res.params.rush_yards * \
            row['rush_yards'] + margin_res.params.rush_yards_allowed*row['rush_yards_allowed'] + \
            margin_res.params.sacked*row['sacked'] + margin_res.params.sacks*row['sacks'] + \
            margin_res.params.takeaways*row['takeaways'] + margin_res.params.total_yards*row['total_yards'] + \
            margin_res.params.total_yards_allowed*row['total_yards_allowed'] + margin_res.params.turnovers * \
            row['turnovers'] + ha_coeff + team_coeff + opp_coeff

        margins.append(margin_predict)

    away_margin = margins[0] + margins[1]
    home_margin = -1*away_margin
    pred_margins = [home_margin, away_margin]

    return pred_margins


def predict_totals(nfl):

    total_res = load_pickle("models/total_res.pickle")

    total_ari_score = 0
    total_ari_opp = 0
    totals = []

    for key, row in nfl.iterrows():
        if row.team == "ARI":
            team_coeff = total_ari_score
        else:
            res_team = "team[T." + row.team + "]"
            team_coeff = total_res.params[res_team]
        if row.opp == "ARI":
            opp_coeff = total_ari_opp
        else:
            res_opp = "team[T." + row.opp + "]"
            opp_coeff = total_res.params[res_opp]
        if row.ha == "away":
            ha_coeff = total_res.params["ha[T.home]"]*-1
        else:
            ha_coeff = total_res.params["ha[T.home]"]*1

        total_predict = total_res.params.Intercept + total_res.params.third_per*row['third_per'] + \
            total_res.params.third_per_allowed*row['third_per_allowed'] + total_res.params.TOP*row['TOP'] + \
            total_res.params.first_downs*row['first_downs'] + total_res.params.first_downs_allowed*row['first_downs_allowed'] + \
            total_res.params.pass_yards*row['pass_yards'] + total_res.params.pass_yards_allowed*row['pass_yards_allowed'] + \
            total_res.params.penalty_yards*row['penalty_yards'] + total_res.params.plays*row['plays'] + \
            total_res.params.rush_yards*row['rush_yards'] + total_res.params.rush_yards_allowed*row['rush_yards_allowed'] + \
            total_res.params.sacked*row['sacked'] + total_res.params.sacks*row['sacks'] + total_res.params.takeaways * \
            row['takeaways'] + total_res.params.total_yards*row['total_yards'] + total_res.params.total_yards_allowed * \
            row['total_yards_allowed'] + total_res.params.turnovers * \
            row['turnovers'] + ha_coeff + team_coeff + opp_coeff

        totals.append(total_predict)

    total_predicted = (totals[0] + totals[1])/2
    pred_totals = [total_predicted, total_predicted]

    return totals, pred_totals


def run_score_model(nfl, team, opponent):

    pred_margins = predict_margins(nfl)
    totals, pred_totals = predict_totals(nfl)

    pred_pfs = []
    pred_pas = []

    for x in np.arange(len(totals)):
        pred_margin = pred_margins[x]
        pred_total = pred_totals[x]
        a = np.array([[1, 1], [1, -1]])
        b = np.array([[pred_total], [pred_margin]])
        points = np.linalg.solve(a, b)
        pf = (points[0][0])
        pa = (points[1][0])
        pred_pfs.append(pf)
        pred_pas.append(pa)

    data = {}

    team_points = int(round(pred_pfs[0]))
    opponent_points = int(round(pred_pas[0]))
    margin = abs(team_points - opponent_points)

    data["team"] = team
    data["team_points"] = team_points
    data["opponent"] = opponent
    data["opponent_points"] = opponent_points
    data["margin"] = margin

    # print(f'{team} {team_points} @ {opponent} {opponent_points}')

    return data
