import config
from kisseklyv import app
from kisseklyv import forms
import flask
import requests

@app.route("/", methods=["GET", "POST"])
@app.route("/index", methods=["GET", "POST"])
def index():
    form = forms.CreateKisseForm()
    if form.validate_on_submit():
        cfg = config.Config()
        post_data = requests.post(f"{cfg.BACKEND_URL}/kisse", data={"description": form.description.data})
        kisse_id = post_data.json()["id"]
        return flask.redirect(flask.url_for("kisse", kisse_id=kisse_id))
    return flask.render_template("start.html", form=form)


@app.route("/kisse/<kisse_id>", methods=["GET", "POST"])
def kisse(kisse_id):
    cfg = config.Config()

    add_person_form = forms.AddPersonForm()
    if add_person_form.validate_on_submit():
        post_data = requests.post(f"{cfg.BACKEND_URL}/person", data={"name": add_person_form.name.data,
                                                                     "kisse_id": kisse_id})
        return flask.redirect(flask.url_for("kisse", kisse_id=kisse_id))

    kisse_data = requests.get(f"{cfg.BACKEND_URL}/kisse", data={"id": kisse_id})
    json_data = kisse_data.json()
    people = [person["name"] for person in json_data["people"]]
    expenses = get_expenses_from_kisse_json(json_data)

    add_expense_form = forms.AddExpenseForm()
    add_expense_form.payer.choices = [(p["id"], p["name"]) for p in json_data["people"]]

    if add_expense_form.validate_on_submit():
        data = {"description": add_expense_form.description.data,
                "amount": add_expense_form.amount.data,
                "person_id": add_expense_form.payer.data}
        print(data)
        post_data = requests.post(f"{cfg.BACKEND_URL}/expense", data)
        return flask.redirect(flask.url_for("kisse", kisse_id=kisse_id))

    klyv_kisse_form = forms.KlyvKisseForm()
    if klyv_kisse_form.validate_on_submit():
        print("klyv")
        return flask.redirect(flask.url_for("klyv", kisse_id=kisse_id))

    return flask.render_template("kisse.html",
                                 description=json_data["description"],
                                 people=people,
                                 expenses=expenses,
                                 add_person_form=add_person_form,
                                 add_expense_form=add_expense_form,
                                 klyv_kisse_form=klyv_kisse_form)


@app.route("/klyv/<kisse_id>", methods=["GET"])
def klyv(kisse_id):
    cfg = config.Config()

    klyv = requests.get(f"{cfg.BACKEND_URL}/kisseklyv", data={"kisse_id": kisse_id})
    kisse = requests.get(f"{cfg.BACKEND_URL}/kisse", data={"id": kisse_id})
    payments = klyv.json()["payments"]
    for payment in payments:
        payment["amount"] = round(payment["amount"], ndigits=2)
    return flask.render_template("kisseklyv.html", kisse_name=kisse.json()["description"],
                                 kisse_id=kisse.json()["id"],
                                 payments=payments)


def get_expenses_from_kisse_json(kisse_json):
    expenses = []
    for person in kisse_json["people"]:
        for expense in person["expenses"]:
            expenses.append({"person": person["name"], "amount": expense["amount"],
                             "description": expense["description"]})
    return expenses

