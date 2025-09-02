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


#Application to run Flask
if __name__ == '__main__':
    app.run(debug=True)