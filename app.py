from flask import Flask, request, render_template, redirect, jsonify
import pandas as pd
from build_dataframe import default_features, form_data


app = Flask(__name__)


@app.route("/")
def home():

    return render_template("index.html")


@app.route("/test-survey")
def test_survey():
    form = {}

    teams = ["ARI", "ATL", "BAL", "BUF", "CAR", "CHI", "CIN", "CLE", "DAL", "DEN", "DET", "GBP",
             "HOU", "IND", "JAX", "KCC", "LAC", "LAR", "MIA", "MIN", "NEP", "NOS", "NYG", "NYJ",
             "OAK", "PHI", "PIT", "SEA", "SFO", "TBB", "TEN", "WAS"]

    form["teams"] = teams
    form["form_data"] = form_data

    return render_template("survey.html", form=form)


@app.route("/send", methods=["GET", "POST"])
def send():
    if request.method == "POST":
        data = {}

        team = request.form["team"]
        opponent = request.form["opponent"]
        third = request.form["third"]
        third_allowed = request.form["third-allowed"]
        top = request.form["top"]
        first_downs = request.form["first-downs"]
        first_downs_allowed = request.form["first-downs-allowed"]
        ha = request.form["ha"]
        pass_yards = request.form["pass-yards-allowed"]
        pass_yards_allowed = request.form["pass-yards-allowed"]
        penalty_yards = request.form["penalty-yards"]
        plays = request.form["plays"]
        rush_yards = request.form["rush-yards"]
        rush_yards_allowed = request.form["rush_yards_allowed"]
        sacked = request.form["sacked"]
        sacks = request.form["sacks"]
        takeaways = request.form["takeaways"]
        total_yards = request.form["total-yards"]
        total_yards_allowed = request.form["total-yards-allowed"]
        turnovers = request.form["turnovers"]

        features = [team, opponent, third, third_allowed, top, first_downs,
                    first_downs_allowed, ha, pass_yards, pass_yards_allowed, penalty_yards, plays,
                    rush_yards, rush_yards_allowed, sacked, sacks, takeaways, total_yards,
                    total_yards_allowed, turnovers]

        for feature in features:
            data[f"{feature}"] = feature

        default_df = pd.DataFrame(default_features)

        return render_template("result.html", data=data)


@app.route("/data")
def data():

    path = "data/nfl_2017.csv"

    df = pd.read_csv(path, encoding="utf-8")

    football_data = df.to_dict(orient="records")

    return jsonify(football_data)


@app.route("/data-prediction")
def data_2015_2017():

    path = "data/nfl_neural_prediction.csv"

    df = pd.read_csv(path, encoding="utf-8")

    football_data = df.to_dict(orient="records")

    return jsonify(football_data)


if __name__ == "__main__":
    app.run(debug=True)
