from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired


# playlist artist form
class PlaylistForm(FlaskForm):
    artist1 = StringField("First Artist", validators=[DataRequired()])
    artist2 = StringField("Second Artist", validators=[DataRequired()])
    artist3 = StringField("Third Artist", validators=[DataRequired()])
    artist4 = StringField("Fourth Artist", validators=[DataRequired()])
    artist5 = StringField("Fifth Artist", validators=[DataRequired()])
    submit = SubmitField("Check My Vibe!")
