from flask import Blueprint, render_template, request, redirect, url_for

from models.base import Session
from models.pizza import Pizza
from models.ingredient import Ingredient
from data.wheather import get_wheather
from db.base import Session, create_db
from db.models import Review, Grade
from forms.forms import ReviewsForm


pizza_route = Blueprint("pizzas", __name__)


@pizza_route.get("/")
def index():
    wheather = get_wheather("Neratovice")

    if 26 > wheather.get("temp") > 10:
        pizza_name = "Тепла"
    elif wheather.get("temp") <= 10:
        pizza_name = "Холодна"
    elif wheather.get("temp") > 26:
        pizza_name = "Пепероні"

    return render_template("index.html", title="Моя супер піцерія", wheather=wheather, pizza_name=pizza_name)


@pizza_route.get("/menu/")
def menu():
    wheather = get_wheather("Kyiv")
    with Session() as session:
        pizzas = session.query(Pizza).all()
        ingredients = session.query(Ingredient).all()

        context = {
            "pizzas": pizzas,
            "ingredients": ingredients,
            "title": "Мега меню",
            "wheather": wheather
        }
        return render_template("menu.html", **context)


@pizza_route.post("/add_pizza/")
def add_pizza():
    with Session() as session:
        name = request.form.get("name")
        price = request.form.get("price")

        ingredients = request.form.getlist("ingredients")
        ingredients = session.query(Ingredient).where(Ingredient.id.in_(ingredients)).all()

        pizza = Pizza(name=name, price=price, ingredients=ingredients)
        session.add(pizza)
        session.commit()
        return redirect("/menu/")
    

@pizza_route.get("/pizza/del/<int:id>/")
def del_pizza(id):
    with Session() as session:
        pizza = session.query(Pizza).where(Pizza.id == id).first()
        session.delete(pizza)
        session.commit()
        return redirect(url_for("pizza.index"))
    

@pizza_route.get("/pizza/edit/<int:id>/")
@pizza_route.post("/pizza/edit/<int:id>/")
def edit_pizza(id):
    with Session() as session:
        pizza = session.query(Pizza).where(Pizza.id == id).first()
        if request.method == "PIZZA":
            name= request.form.get("iname")
            price = request.form.get("price")

            pizza.name = name
            pizza.price = price
            session.commit()
            return redirect(url_for("pizza.index"))

        return render_template("edit_pizza.html", pizza=pizza, wheather=get_wheather())
    

@pizza_route.get("/poll")
def poll():
    with Session() as session:
        pizzas = session.query(Pizza).all()
        question = "Яка вам сподобаласб най бвльше?"
    return render_template("poll.html", question=question, pizzas=pizzas)


@pizza_route.get("/add_vote/")
def add_vote():
    pizza = request.args.get("pizza")

    with open("data/answers.txt", "a", encoding="utf-8") as file:
        file.write(pizza + "\n")


        return redirect(url_for("pizzas.results"))
    

@pizza_route.get("/results/")
def results():
    with open("data/answers.txt", "r", encoding="utf-8") as file:
        answers = file.readlines()



    return render_template("results.html", answers=answers)




@pizza_route.route("/review/", methods=["GET", "POST"])
def add_review():
    with Session() as session:
        form = ReviewsForm()
        grades = session.query(Grade).all()
        if request.method == "POST":
            grade_id = form.grade.data
            text = form.text.data
            author = form.author.data

            review = Review(text=text, author=author, grade_id=grade_id)
            session.add(review)
            session.commit()
            return redirect("/reviews/")
        
        form.grade.choices = []
        for grade in grades:
            form.grade.choices.append((grade.id, grade.value))
        return render_template("add_review.html", form=form)
    




@pizza_route.get("/reviews/")
def show_reviews():
    with Session() as session:
        reviews = session.query(Review).all()
        return render_template("reviews.html", reviews)

