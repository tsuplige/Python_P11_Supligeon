import json
from flask import Flask, render_template, request, redirect, flash, url_for
from datetime import datetime


def loadClubs():
    with open("clubs.json") as c:
        listOfClubs = json.load(c)["clubs"]
        return listOfClubs


def loadCompetitions():
    with open("competitions.json") as comps:
        listOfCompetitions = json.load(comps)["competitions"]
        return listOfCompetitions


def verifyCompetitionDate(competition_date):
    try:
        format_date = datetime.strptime(competition_date, '%Y-%m-%d %H:%M:%S')
    except ValueError:
        print(" date érronée ou non au format: '%Y-%m-%d %H:%M:%S'")
        return False
    date_now = datetime.now()

    if format_date > date_now:
        return True
    return False


app = Flask(__name__)
app.secret_key = "something_special"

competitions = loadCompetitions()
clubs = loadClubs()

for comp in competitions:
    comp['IsFuturComp'] = verifyCompetitionDate(comp['date'])


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/showSummary", methods=["POST"])
def showSummary():
    try:
        club = [club for club in clubs if club["email"] == request.form["email"]][0]
        return render_template("welcome.html", club=club,
                               competitions=competitions)
    except IndexError:
        flash("like the email isn't found")
        return render_template("index.html"), 404


@app.route("/book/<competition>/<club>")
def book(competition, club):
    foundClub = [c for c in clubs if c["name"] == club][0]
    foundCompetition = [c for c in competitions if c["name"] == competition][0]
    if foundClub and foundCompetition:
        return render_template(
            "booking.html", club=foundClub, competition=foundCompetition
        )
    else:
        flash("Something went wrong-please try again")
        return render_template("welcome.html", club=club,
                               competitions=competitions)


@app.route("/purchasePlaces", methods=["POST"])
def purchasePlaces():
    try:
        club = [c for c in clubs if c["name"] == request.form["club"]][0]
    except IndexError:
        flash("The club does not exist in database")
        return render_template("index.html"), 404

    try:
        competition = [
            c for c in competitions if c["name"] == request.form["competition"]
        ][0]
    except IndexError:
        flash("The competition does not exist in database")
        return (
            render_template("welcome.html", club=club, competitions=competitions),
            404,
        )
    try:
        placesRequired = int(request.form["places"])
    except ValueError:
        flash("number places not specified")
        return (
            render_template("welcome.html", club=club,
                            competitions=competitions),
            400,
        )
    if (
        int(club["points"]) - placesRequired >= 0
        and placesRequired <= 12
        and placesRequired <= int(competition["numberOfPlaces"])
    ):
        club["points"] = str(int(club["points"]) - placesRequired)
        competition["numberOfPlaces"] = (
            int(competition["numberOfPlaces"]) - placesRequired
        )
    elif placesRequired > 12:
        flash("you can't purchase more than 12 places")
        return (
            render_template("welcome.html", club=club,
                            competitions=competitions),
            403,
        )
    elif placesRequired > int(competition["numberOfPlaces"]):
        flash("You cannot purchase more than the available places")
        return (
            render_template("welcome.html", club=club,
                            competitions=competitions),
            403,
        )
    else:
        flash(
            f"The club does not have enough " f"points to order {placesRequired} seats."
        )
        return (
            render_template("welcome.html", club=club, competitions=competitions),
            403,
        )
    flash("Great-booking complete!")
    return render_template("welcome.html", club=club, competitions=competitions), 200


# TODO: Add route for points display


@app.route("/logout")
def logout():
    return redirect(url_for("index"))
