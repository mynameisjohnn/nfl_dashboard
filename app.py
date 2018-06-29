from flask import Flask, request, render_template, redirect, jsonify
import pandas as pd


app = Flask(__name__)


@app.route("/")
def home():

    return render_template("index.html")


@app.route("/test-survey")
def test_survey():

    return render_template("survey.html")


@app.route("/result", methods=["GET", "POST"])
def send():
    if request.method == "POST":
        data = {}

        team = request.form["team"]
        opponent = request.form["opponent"]
        sacked = request.form["sacked"]

        data["team"] = team
        data["opponent"] = opponent
        data['sacked'] = sacked

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
