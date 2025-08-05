from flask import Flask, render_template
from datetime import datetime
import sqlite3

#Creates Flask Application
app = Flask(__name__)

def get_db():
    db= sqlite3.connect('food.db')
    db.row_factory = sqlite3.Row

    return db

@app.route('/')
def home():
    conn = sqlite3.connect('food.db')
    cur = conn.cursor()
    cur.execute('SELECT * FROM menu_items')
    food = cur.fetchall()
    conn.close()
    return render_template('home.html', title='HOME', food = food)




#Route to show all foods avaiable in hot food.
@app.route('/hot_food')
def all_hot_food():
    conn = sqlite3.connect('food.db')
    cur = conn.cursor()
    cur.execute('SELECT * FROM menu_items WHERE category="Hot Food (every day)"')
    hot_food = cur.fetchall()
    conn.close()
    return render_template('hot_food.html', title='HOME', hot_food = hot_food)

if __name__ == '__main__':
    app.run(debug=True)