import os
from flask import Flask, render_template, redirect, url_for, request
from flask_pymongo import PyMongo
from bson.objectid import ObjectId

if os.path.exists("env.py"):
    import env


app = Flask(__name__)

app.config["MONGO_DBNAME"] = "cook"
app.config["MONGO_URI"] = os.environ['MONGO_URI']
mongo = PyMongo(app)


# ------ recipes ------ #


@app.route('/')
@app.route('/get_recipes')
def get_recipes():
    return render_template('recipes.html', recipes=mongo.db.recipes.find())


@app.route('/add_recipe')
def add_recipe():
    _categories = mongo.db.categories.find()
    category_list = [category for category in _categories]
    return render_template("addrecipe.html", categories=category_list)


@app.route('/insert_recipe', methods=['POST'])
def insert_recipe():
    recipes = mongo.db.recipes
    recipes.insert_one(request.form.to_dict())
    return redirect(url_for('get_recipes'))


@app.route('/edit_recipe/<recipe_id>')
def edit_recipe(recipe_id):
    the_recipe = mongo.db.recipes.find_one({"_id": ObjectId(recipe_id)})
    all_categories = mongo.db.categories.find()
    return render_template('editrecipe.html', recipe=the_recipe, categories=all_categories)


# ------ categories ------ #


@app.route('/get_categories')
def get_categories():
    return render_template('home.html',
    categories=mongo.db.categories.find())


@app.route('/get_cookbook')
def get_cookbook():
    return render_template('cookbook.html',
    cook_book=mongo.db.cook_book.find())



if __name__ == "__main__":
    app.run(host=os.environ.get("IP", "0.0.0.0"),
            port=os.environ.get("PORT", "5000"),
            debug=True)