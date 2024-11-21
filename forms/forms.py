from flask_wtf import FlaskForm
import wtforms

class ReviewsForm(FlaskForm):
    grade = wtforms.RadioField("оберіть очінку")
    text = wtforms.TelField("Ввідіть свій відгік")
    author = wtforms.StringField("як тібя зівут")
    submit = wtforms.SubmitField("Збірігті")
