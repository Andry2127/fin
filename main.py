from flask import Flask, render_template, request, redirect

from routes.pizza import pizza_route
from models.pizza import Pizza
from models.ingredient import Ingredient
from models.base import create_db
from db.base import Session, create_db
from db.models import Review, Grade
from forms.forms import ReviewsForm

app = Flask(__name__)
app.register_blueprint(pizza_route)
app.secret_key="1233"

    

if __name__ == "__main__":
    create_db()
    app.run(debug=True, port=5052)