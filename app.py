from flask import Flask, render_template, jsonify
import pandas as pd


app = Flask(__name__)


@app.route("/")
def home():

    return render_template("index.html")


@app.route("/data")
def data():

    path = "data/nfl_2017.csv"

    df = pd.read_csv(path, encoding="utf-8")

    football_data = df.to_dict(orient="records")

    return jsonify(football_data)


if __name__ == "__main__":
    app.run(debug=True)
