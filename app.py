from flask import Flask, request, render_template, jsonify
import pandas as pd
from keras.models import load_model
from build_dataframe import get_default_df, form_names, teams_abbrev


app = Flask(__name__)


def run_model(model_input_df, team, opponent):
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
                data["winner"] = team
            elif key == team:
                data["loser"] = opponent

    return data


@app.route("/")
def home():

    return render_template("index.html")


@app.route("/predictions")
def predict():

    return render_template("prediction_model.html")


@app.route("/send", methods=["GET", "POST"])
def send():
    if request.method == "POST":

        team = request.form["team"]
        opponent = request.form["opp"]
        third = float(request.form["third_per"])
        third_allowed = float(request.form["third_per_allowed"])
        top = float(request.form["TOP"])
        first_downs = float(request.form["first_downs"])
        first_downs_allowed = float(request.form["first_downs_allowed"])
        ha = request.form["ha"]
        pass_yards = float(request.form["pass_yards"])
        pass_yards_allowed = float(request.form["pass_yards_allowed"])
        penalty_yards = float(request.form["penalty_yards"])
        plays = float(request.form["plays"])
        rush_yards = float(request.form["rush_yards"])
        rush_yards_allowed = float(request.form["rush_yards_allowed"])
        sacked = float(request.form["sacked"])
        sacks = float(request.form["sacks"])
        takeaways = float(request.form["takeaways"])
        total_yards = float(request.form["total_yards"])
        total_yards_allowed = float(request.form["total_yards_allowed"])
        turnovers = float(request.form["turnovers"])

        feature_values = [team, opponent, third, third_allowed, top, first_downs,
                          first_downs_allowed, ha, pass_yards, pass_yards_allowed, penalty_yards,
                          plays, rush_yards, rush_yards_allowed, sacked, sacks, takeaways,
                          total_yards, total_yards_allowed, turnovers]

        default_df = get_default_df()

        model_input_df = default_df.copy()

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

        data = run_model(model_input_df, team, opponent)

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
