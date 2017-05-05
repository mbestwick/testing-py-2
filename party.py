"""Flask site for Balloonicorn's Party."""


from flask import Flask, session, render_template, request, flash, redirect
from flask_debugtoolbar import DebugToolbarExtension
from model import Game, connect_to_db, db

app = Flask(__name__)
app.secret_key = "SECRETSECRETSECRET"


@app.route("/")
def homepage():
    """Show homepage."""

    return render_template("homepage.html")


@app.route("/rsvp", methods=['POST'])
def rsvp():
    """Register for the party."""

    name = request.form.get("name")
    email = request.form.get("email")

    session['RSVP'] = True
    flash("Yay!")
    return redirect("/")


@app.route("/games")
def games():

    if 'RSVP' in session:
        games = Game.query.all()
        return render_template("games.html", games=games)
    else:
        flash("YOU MUST LOGIN TO SEE THE GAMES!!!!")
        return redirect("/")


@app.route("/games", methods=["POST"])
def add_game():
    new_game = request.form.get("game_name")
    new_game_description = request.form.get("game_description")

    g = Game(name=new_game, description=new_game_description)
    db.session.add(g)
    db.session.commit()

    flash("Game successfully added!")
    return redirect("/games")


@app.route("/game-delete", methods=["POST"])
def delete_game():
    game = request.form.get("game_name")

    game_object = Game.query.filter(Game.name == game).one()
    db.session.delete(game_object)
    db.session.commit()

    flash("Game successfully deleted :(")
    return redirect("/games")


if __name__ == "__main__":
    app.debug = True
    app.config['DEBUG_TB_INTERCEPT_REDIRECTS'] = False
    DebugToolbarExtension(app)
    connect_to_db(app)
    app.run()
