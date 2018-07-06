from flask import Flask, request, render_template, redirect, url_for, jsonify, flash
import pandas as pd
from forms import PredictionForm
from run_models import get_default_df, form_names, form_select, run_win_loss_model, run_score_model


app = Flask(__name__)
app.config["SECRET_KEY"] = "f6d8e6606333c3bb49dbee9d786e3ca7"


@app.route("/")
def home():
    return render_template("index.html")


@app.route("/predictions")
def predict():
    form = PredictionForm()
    select_options = [(key, value) for key, value in form_select.items()]
    form.team.choices = select_options
    form.opp.choices = select_options

    return render_template("prediction_model.html", form=form)


@app.route("/results", methods=["GET", "POST"])
def results():
    if request.method == "POST":
        if request.form["team"] == "default" or request.form["opp"] == "default":
            flash("Please pick two teams.", "danger")
            return redirect(url_for("predict"))
        elif request.form["team"] == request.form["opp"]:
            flash("A team cannot play with itself.", "danger")
            return redirect(url_for("predict"))

        try:
            team = request.form["team"]
            opponent = request.form["opp"]
            third_per = float(request.form["third_per"])
            third_per_allowed = float(request.form["third_per_allowed"])
            top = float(request.form["top"])
            a_top = float(request.form["a_top"])
            first_downs = float(request.form["first_downs"])
            first_downs_allowed = float(request.form["first_downs_allowed"])
            pass_yards = float(request.form["pass_yards"])
            pass_yards_allowed = float(request.form["pass_yards_allowed"])
            penalty_yards = float(request.form["penalty_yards"])
            a_penalty_yards = float(request.form["a_penalty_yards"])
            plays = float(request.form["plays"])
            a_plays = float(request.form["a_plays"])
            rush_yards = float(request.form["rush_yards"])
            rush_yards_allowed = float(request.form["rush_yards_allowed"])
            sacked = float(request.form["sacked"])
            sacks = float(request.form["sacks"])
            takeaways = float(request.form["takeaways"])
            total_yards = float(request.form["total_yards"])
            total_yards_allowed = float(request.form["total_yards_allowed"])
            turnovers = float(request.form["turnovers"])
        except ValueError:
            flash("Input fields must be numbers.", "danger")
            return redirect(url_for("predict"))
        except KeyError:
            flash("Please fill out all fields.", "danger")
            return redirect(url_for("predict"))

        try:
            chosen_model = request.form["model_name"]
        except KeyError:
            flash("Please choose a model.", "danger")
            return redirect(url_for("predict"))

        if chosen_model == "winloss":
            # Deep neural network model
            feature_values = [team, opponent, third_per, third_per_allowed, top, first_downs,
                              first_downs_allowed, pass_yards, pass_yards_allowed, penalty_yards,
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

            data = run_win_loss_model(model_input_df, team, opponent)

            return render_template("results_neural.html", data=data)

        elif chosen_model == "score":
            # Score model
            home_dictionary = {"ha": "home", "team": team, "opp": opponent, "third_per": third_per, "third_per_allowed": third_per_allowed,
                               "TOP": top, "first_downs": first_downs, "first_downs_allowed": first_downs_allowed, "pass_yards": pass_yards,
                               "pass_yards_allowed": pass_yards_allowed, "penalty_yards": penalty_yards, "plays": plays,
                               "rush_yards": rush_yards, "rush_yards_allowed": rush_yards_allowed, "sacks": sacks, "sacked": sacked,
                               "takeaways": takeaways, "turnovers": turnovers, "total_yards": total_yards,
                               "total_yards_allowed": total_yards_allowed}

            away_dictionary = {"ha": "away", "team": opponent, "opp": team, "third_per": third_per_allowed, "third_per_allowed": third_per,
                               "TOP": a_top, "first_downs": first_downs_allowed, "first_downs_allowed": first_downs,
                               "pass_yards": pass_yards_allowed, "pass_yards_allowed": pass_yards, "penalty_yards": a_penalty_yards,
                               "plays": a_plays, "rush_yards": rush_yards_allowed, "rush_yards_allowed": rush_yards, "sacks": sacked,
                               "sacked": sacks, "takeaways": turnovers, "turnovers": takeaways, "total_yards": total_yards_allowed,
                               "total_yards_allowed": total_yards}

            stats_dicts = [home_dictionary, away_dictionary]

            nfl = pd.DataFrame(stats_dicts)

            data = run_score_model(nfl, team, opponent)

            return render_template("results_score.html", data=data)
        else:
            return redirect(url_for("predict"))


@app.route("/teams-data")
def teams_data():

    df = pd.read_csv("data/teams.csv")

    data = df.to_dict(orient="records")

    return jsonify(data)


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
