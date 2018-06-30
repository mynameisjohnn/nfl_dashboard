from flask import Flask, request, render_template, redirect, jsonify
import pandas as pd
from build_dataframe import default_features, form_data


app = Flask(__name__)


@app.route("/")
def home():

    return render_template("index.html")


@app.route("/predictions")
def predict():


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
        rush_yards_allowed = request.form["rush-yards-allowed"]
        sacked = request.form["sacked"]
        sacks = request.form["sacks"]
        takeaways = request.form["takeaways"]
        total_yards = request.form["total-yards"]
        total_yards_allowed = request.form["total-yards-allowed"]
        turnovers = request.form["turnovers"]

        # form_names = ["team", "opponent", "third", "third-allowed", "top", "first-downs",
        #               "first-downs-allowed", "ha", "pass-yards", "pass-yards-allowed", "penalty-yards",
        #               "plays", "rush-yards", "rush-yards-allowed", "sacked", "sacks", "takeaways",
        #               "total-yards", "total-yards-allowed", "turnovers"]

        form_names = []

        for item in form_data:
            form_names.append(item["form_name"])

        feature_values = [team, opponent, third, third_allowed, top, first_downs,
                          first_downs_allowed, ha, pass_yards, pass_yards_allowed, penalty_yards,
                          plays, rush_yards, rush_yards_allowed, sacked, sacks, takeaways,
                          total_yards, total_yards_allowed, turnovers]

        # print(feature_values)

        model_input_dict = {}

        for i in range(len(form_names)):
            model_input_dict[form_names[i]] = feature_values[i]

        print(model_input_dict)

        default_df = pd.DataFrame(default_features)

        columns = list(default_df.columns)

        # Add only keys to data dictionary
        # for column in columns:
        #     data.add(column)

        # Now add values to each key
        # for key in data.keys():

        for value in feature_values:
            data[f"{value}"] = value

        return render_template("result.html", data=data)


@app.route("/data")
def data():


@app.route("/tables")
def tables():

    return render_template("tables.html")


@app.route("/howitworks")
def howitworks():

    return render_template("howitworks.html")


@app.route("/data-prediction")
def data_2015_2017():

    path = "data/nfl_neural_prediction.csv"

    df = pd.read_csv(path, encoding="utf-8")

    football_data = df.to_dict('split')

    return jsonify(football_data)


if __name__ == "__main__":
    app.run(debug=True)
