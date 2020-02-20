from flask_wtf import FlaskForm
from wtforms import SubmitField, StringField, FloatField, SelectField
from wtforms.validators import DataRequired


class CreateKisseForm(FlaskForm):
    description = StringField("Beskrivning", validators=[DataRequired()])
    submit = SubmitField("Skapa en ny Kisse")


class AddPersonForm(FlaskForm):
    name = StringField("Namn", validators=[DataRequired()])
    submit = SubmitField("Lägg till person")


class AddExpenseForm(FlaskForm):
    description = StringField("Beskrivning", validators=[DataRequired()])
    amount = FloatField("Belopp", validators=[DataRequired()])
    payer = SelectField("Betalad av", choices=[])
    submit = SubmitField("Lägg till utlägg")


class KlyvKisseForm(FlaskForm):
    submit = SubmitField("Klyv Kissen!!!")