from flask_wtf import FlaskForm
from wtforms import SelectField, DecimalField, RadioField, SubmitField
from wtforms.validators import InputRequired


class PredictionForm(FlaskForm):
    team = SelectField("Home Team")
    opp = SelectField("Away Team")
    third_per = DecimalField("Third Percentage", validators=[InputRequired()])
    third_per_allowed = DecimalField("Third Percentage", validators=[InputRequired()])
    top = DecimalField("Time of Possession", validators=[InputRequired()])
    a_top = DecimalField("Time of Possession", validators=[InputRequired()])
    first_downs = DecimalField("First Downs", validators=[InputRequired()])
    first_downs_allowed = DecimalField("First Downs", validators=[InputRequired()])
    pass_yards = DecimalField("Pass Yards", validators=[InputRequired()])
    pass_yards_allowed = DecimalField("Pass Yards", validators=[InputRequired()])
    penalty_yards = DecimalField("Penalty Yards", validators=[InputRequired()])
    a_penalty_yards = DecimalField("Penalty Yards", validators=[InputRequired()])
    plays = DecimalField("Plays", validators=[InputRequired()])
    a_plays = DecimalField("Plays", validators=[InputRequired()])
    rush_yards = DecimalField("Rush Yards", validators=[InputRequired()])
    rush_yards_allowed = DecimalField("Rush Yards", validators=[InputRequired()])
    sacked = DecimalField("Sacks", validators=[InputRequired()])
    sacks = DecimalField("Sacks", validators=[InputRequired()])
    turnovers = DecimalField("Turnovers", validators=[InputRequired()])
    takeaways = DecimalField("Turnovers", validators=[InputRequired()])
    total_yards = DecimalField("Total Yards", validators=[InputRequired()])
    total_yards_allowed = DecimalField("Total Yards", validators=[InputRequired()])

    model_name = RadioField("Models", choices=[("winloss", "Win/Loss Prediction Model"), ("score", "Projected Points Prediction Model ")])

    submit = SubmitField("SUBMIT")
