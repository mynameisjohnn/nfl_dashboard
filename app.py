from flask import Flask, request, render_template, jsonify
import pandas as pd
from keras.models import load_model
from build_dataframe import get_default_df, get_form_data


app = Flask(__name__)


@app.route("/")
def home():

    return render_template("index.html")


@app.route("/predictions")
def predict():
    pass


@app.route("/test-survey")
def test_survey():
    form = {}

    teams = ["ARI", "ATL", "BAL", "BUF", "CAR", "CHI", "CIN", "CLE", "DAL", "DEN", "DET", "GBP",
             "HOU", "IND", "JAX", "KCC", "LAC", "LAR", "MIA", "MIN", "NEP", "NOS", "NYG", "NYJ",
             "OAK", "PHI", "PIT", "SEA", "SFO", "TBB", "TEN", "WAS"]

    form["teams"] = teams

    form_data, form_names = get_form_data()

    form["form_data"] = form_data

    return render_template("survey.html", form=form)


@app.route("/send", methods=["GET", "POST"])
def send():
    if request.method == "POST":
        # data = {}

        team = request.form["team"]
        opponent = request.form["opp"]
        third = request.form["third_per"]
        third_allowed = request.form["third_per_allowed"]
        top = request.form["TOP"]
        first_downs = request.form["first_downs"]
        first_downs_allowed = request.form["first_downs_allowed"]
        ha = request.form["ha"]
        pass_yards = request.form["pass_yards"]
        pass_yards_allowed = request.form["pass_yards_allowed"]
        penalty_yards = request.form["penalty_yards"]
        plays = request.form["plays"]
        rush_yards = request.form["rush_yards"]
        rush_yards_allowed = request.form["rush_yards_allowed"]
        sacked = request.form["sacked"]
        sacks = request.form["sacks"]
        takeaways = request.form["takeaways"]
        total_yards = request.form["total_yards"]
        total_yards_allowed = request.form["total_yards_allowed"]
        turnovers = request.form["turnovers"]

        feature_values = [team, opponent, third, third_allowed, top, first_downs,
                          first_downs_allowed, ha, pass_yards, pass_yards_allowed, penalty_yards,
                          plays, rush_yards, rush_yards_allowed, sacked, sacks, takeaways,
                          total_yards, total_yards_allowed, turnovers]

        default_df = get_default_df()

        model_input_df = default_df.copy()

        form_data, form_names = get_form_data()

        model_input_dict = dict(zip(form_names, feature_values))

        columns = list(default_df.columns)

        for column in columns:
            for key, value in model_input_dict.items():

                if key == column:
                    model_input_df[column] = value

                elif f"{key}_{value}" == column:
                    model_input_df[column] = 1

        ha_value = model_input_df["ha"][0]

        if ha_value == "Home":
            model_input_df["ha"] = 0
        elif ha_value == "Away":
            model_input_df["ha"] = 1

        data = model_input_df.to_dict(orient="records")

        # for value in feature_values:
        #     data[f"{value}"] = value

        return render_template("result.html", data=data)


@app.route("/data")
def data():
    pass


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
