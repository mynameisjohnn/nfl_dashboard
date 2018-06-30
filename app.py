from flask import Flask, render_template, jsonify
import pandas as pd


app = Flask(__name__)


@app.route("/")
def home():

    return render_template("index.html")

@app.route("/predictions")
def predict():

    return render_template("prediction_model.html")

@app.route("/tables")
def tables():

    return render_template("tables.html")

@app.route("/howitworks")
def howitworks():

    return render_template("howitworks.html")

@app.route("/data")
def data():
    path = "data/nfl.csv"

    df = pd.read_csv(path, encoding="utf-8")

    football_data = df.to_dict('split')

    return jsonify(football_data)

if __name__ == "__main__":
    app.run(debug=True)
