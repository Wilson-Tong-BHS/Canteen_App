from flask import Flask, render_template
import sqlite3

#Creates Flask Application
app = Flask(__name__)

def get_menu_data():
    conn = sqlite3.connect("food.db")
    conn.row_factory = sqlite3.Row
    cur = conn.cursor()

    cur.execute("SELECT DISTINCT category FROM menu_items")
    categories = cur.fetchall()

    menu = []
    for cat in categories:
        category_name = cat["category"]
        cur.execute("SELECT name, price, image_link FROM menu_items WHERE category = ? ORDER by name ASC", (category_name,))
        items = cur.fetchall()

        # Convert each item from Row to dictionary
        menu_list = []
        for item in items:
            menu_list.append({
                "name": item["name"],
                "price": item["price"],
                "image_link": item["image_link"]
            })

        menu.append({
            "id": category_name.lower().replace(" ", "_").replace("(", "").replace(")", "").replace("&", "and"),
            "name": category_name,
            "menu_items": menu_list
        })
        
    conn.close()
    return menu


@app.route("/")
def home():
    categories = get_menu_data()
    return render_template("home.html", categories=categories)


@app.route("/menu")
def menu():
    categories = get_menu_data()
    return render_template("menu_scroll.html", categories=categories)




#Route to show all hot foods avaiable in food database.
@app.route('/hot_food')
def all_hot_food():
    conn = sqlite3.connect('food.db')
    cur = conn.cursor()
    cur.execute('SELECT * FROM menu_items WHERE category="Hot Food (every day)"')
    hot_food = cur.fetchall()
    conn.close()
    return render_template('menu.html', hot_food = hot_food)


#Route to show all sandwich/rolls/wraps avaiable in food database.
@app.route('/sandwich')
def all_sandwich():
    conn = sqlite3.connect('food.db')
    cur = conn.cursor()
    cur.execute('SELECT * FROM menu_items WHERE category="Sandwiches/Rolls/Wraps"')
    sandwich = cur.fetchall()
    conn.close()
    return render_template('menu.html', sandwich = sandwich)


#Route to show all muffin/slices/cookies/cakes avaiable in food database.
@app.route('/muffin')
def all_muffin():
    conn = sqlite3.connect('food.db')
    cur = conn.cursor()
    cur.execute('SELECT * FROM menu_items WHERE category="Muffins/Slices/Cookies/Cakes"')
    muffin = cur.fetchall()
    conn.close()
    return render_template('menu.html', muffin = muffin)


#Route to show all potato chips īn food database
@app.route('/chip')
def all_chip():
    conn = sqlite3.connect('food.db')
    cur = conn.cursor()
    cur.execute('SELECT * FROM menu_items WHERE category="Potato Chips"')
    chip = cur.fetchall()
    conn.close()
    return render_template('menu.html', chip = chip)

#Route to show all salads in food database
@app.route('/salad')
def all_salad():
    conn = sqlite3.connect('food.db')
    cur = conn.cursor()
    cur.execute('SELECT * FROM menu_items WHERE category="Salad (Summer only)"')
    salad = cur.fetchall()
    conn.close()
    return render_template('menu.html', salad = salad)

#Route to show all Hot Food (Different Meal Each Day) in food database
@app.route('/hot_food_different_meal')
def all_hot_food_different_meal():
    conn = sqlite3.connect('food.db')
    cur = conn.cursor()
    cur.execute('SELECT * FROM menu_items WHERE category="Hot Food (Different Meal Each Day)"')
    hot_food_different_meal = cur.fetchall()
    conn.close()
    return render_template('menu.html', hot_food_different_meal = hot_food_different_meal)

#Route to show all cold drinks in food database
@app.route('/cold_drink')
def all_cold_drink():
    conn = sqlite3.connect('food.db')
    cur = conn.cursor()
    cur.execute('SELECT * FROM menu_items WHERE category="Cold Drinks"')
    cold_drink = cur.fetchall()
    conn.close()
    return render_template('menu.html', cold_drink=cold_drink)

#Route to show all ice creams in food database
@app.route('/ice_cream')
def all_ice_cream():
    conn = sqlite3.connect('food.db')
    cur = conn.cursor()
    cur.execute('SELECT * FROM menu_items WHERE category="Ice Creams"')
    ice_cream= cur.fetchall()
    conn.close()
    return render_template('menu.html', ice_cream = ice_cream)


#Route to show all fruit & Yoghurt in food database
@app.route('/yoghurt_fruit')
def all_yoghurt_fruit():
    conn = sqlite3.connect('food.db')
    cur = conn.cursor()
    cur.execute('SELECT * FROM menu_items WHERE category="Fruit & Yoghurt"')
    yoghurt_fruit = cur.fetchall()
    conn.close()
    return render_template('menu', yoghurt_fruit= yoghurt_fruit)

#Route to show all hot drinks in food database
def all_hot_drink():
    conn = sqlite3.connect('food.db')
    cur = conn.cursor()
    cur.execute('SELECT * FROM menu_items WHERE category="Hot Drinks"')
    hot_drink = cur.fetchall()
    conn.close()
    return render_template('menu', hot_drink = hot_drink)


#Application to run Flask
if __name__ == '__main__':
    app.run(debug=True)