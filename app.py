from flask import Flask, request, render_template, redirect, flash, session
from flask_debugtoolbar import DebugToolbarExtension
from models import db, connect_db, User

app = Flask(__name__)

# order matter, this comes first
# this connects to database
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///user_db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_ECHO'] = True
app.config['SECRET_KEY'] = "This is demo"
app.config['DEBUG_TB_INTERCEPT_REDIRECTS'] = False
deubg = DebugToolbarExtension(app)

connect_db(app)


@app.route('/')
def root():

    return redirect('/users')


@app.route('/users')
def list_users():
    """Shows list of all pets in db"""
    users = User.query.all()
    return render_template('list.html', users=users)


@app.route('/users/new')
def add_user_form():
    """Show form to add user"""
    return render_template('add_user.html')


@app.route('/users/new', methods=["POST"])
def create_user():
    firstname = request.form['firstname']
    lastname = request.form['lastname']
    imgurl = request.form['imageurl']

    new_user = User(first_name=firstname, last_name=lastname, image_url=imgurl)
    db.session.add(new_user)
    db.session.commit()
    return redirect('/users')


@app.route('/users/<int:user_id>')
def show_user(user_id):
    """Show user profile"""
    user = User.query.get_or_404(user_id)
    return render_template("profile.html", user=user)


@app.route('/users/<int:user_id>/edit')
def edit_page(user_id):
    """Edit user info"""
    user = User.query.get_or_404(user_id)
    return render_template('edit_user.html', user=user)


@app.route('/users/<int:user_id>/edit', methods=["POST"])
def edit_user(user_id):
    user = User.query.get(user_id)
    user.first_name = request.form['firstname']
    user.last_name = request.form['lastname']
    user.image_url = request.form['imageurl']
    db.session.add(user)
    db.session.commit()
    return redirect('/users')


@app.route('/users/<int:user_id>/delete', methods=["POST"])
def delete_user(user_id):
    user = User.query.get_or_404(user_id)
    db.session.delete(user)
    db.session.commit()
    return redirect('/users')

# @app.route('/', methods=["POST"])
# def create_pet():
#     """"""
#     name = request.form["name"]
#     species = request.form["species"]
#     hunger = request.form["hunger"]
#     hunger = int(hunger) if hunger else None

#     new_pet = Pet(name=name, species=species, hunger=hunger)
#     db.session.add(new_pet)
#     db.session.commit()

#     return redirect(f"/{new_pet.id}")


# @app.route('/<int:pet_id>')
# def show_pet(pet_id):
#     """Show details about a single pet"""
#     pet = Pet.query.get_or_404(pet_id)
#     return render_template("details.html", pet=pet)

# @app.route('/species/<species_id>')
# def show_pets_by_species(species_id):
#     """"""
#     pets = Pet.get_by_species(species_id)
#     return render_template('species.html', pets=pets, species=species_id)
