"""This routes.py contains routes for flask applications and functions to get data from the database food.db
    Created by Wilson Tong
 """

from flask import Flask, render_template
import sqlite3

# Creates Flask Application
app = Flask(__name__)


'''Function to get menu categories and items'''


def get_menu_data():
    conn = sqlite3.connect("food.db")
    # row factory to access columns by name
    conn.row_factory = sqlite3.Row
    cur = conn.cursor()

    # get all the food categories in the database
    cur.execute("SELECT DISTINCT category FROM menu_items")
    categories = cur.fetchall()

    # get the menu items from categories
    menu = []
    for cat in categories:
        category_name = cat["category"]
        cur.execute(
            "SELECT id, name, price, image_link FROM menu_items "
            "WHERE category = ?",
            (category_name,)
        )
        items = cur.fetchall()

        # turn each item from Row to dictionary
        menu_list = []
        # creates a loop to repeat each item
        for item in items:
            menu_list.append({
                "id": item["id"],
                "name": item["name"],
                "price": item["price"],
                "image_link": item["image_link"]
            })
        # Changes category name to a valid name for HTML id
        menu.append({
            "id": (
                category_name.lower()
                .replace(" ", "_")
                .replace("(", "")
                .replace(")", "")
            ),
            # Display name
            "name": category_name,
            # Display menu items
            "menu_items": menu_list
            })
    conn.close()
    return menu


'''Function to get information about menu items'''


def get_menu_info(item_id):
    conn = sqlite3.connect("food.db")
    conn.row_factory = sqlite3.Row
    cur = conn.cursor()

    # SQL query to get information about  menu item by id
    cur.execute(
        "SELECT f.image_link, f.name, f.price, f.description, "
        "GROUP_CONCAT(ho.name, ',') AS healthy_options "
        "FROM menu_items f "
        "LEFT JOIN FoodHealthyOption fho ON f.id = fho.food_id "
        "LEFT JOIN HealthyOption ho ON fho.health_id = ho.health_id "
        "WHERE f.id = ? "
        "GROUP BY f.id",
        (item_id,)
    )
    menu_info = cur.fetchone()
    conn.close()
    return menu_info


# error handler for 404 errors
@app.errorhandler(404)
def http_error_handler(error):
    return render_template("404.html"), 404


# Route for home page
@app.route("/")
def home():
    categories = get_menu_data()
    return render_template("home.html", categories=categories)


# Route for menu page
@app.route("/menu")
def menu():
    categories = get_menu_data()
    return render_template("menu_scroll.html", categories=categories)


# Route for item details page
@app.route('/item/<int:item_id>')
def item_detail(item_id):
    try:
        item_detail = get_menu_info(item_id)
        if item_detail:
            return render_template('item_detail.html', item=item_detail)
        else:
            return render_template('404.html'), 404
    # Catch OverflowError if item_id is too large
    except OverflowError:
        return render_template('404.html'), 404


# Application to run Flask
if __name__ == '__main__':
    app.run(debug=True)
