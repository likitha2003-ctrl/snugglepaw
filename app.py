from flask import Flask, render_template, request, redirect
import sqlite3
app = Flask(__name__)

# Create connection to SQLite database
def create_connection():
    conn = sqlite3.connect("users2.db")
    return conn

# Create table to sre users
def create_table():
    conn = create_connection()
    cur = conn.cursor()
    cur.execute('''
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            full_name TEXT NOT NULL,
            dog_name TEXT NOT NULL,
            dog_breed TEXT NOT NULL,
            email TEXT UNIQUE NOT NULL,
            password TEXT NOT NULL
        )
    ''')
    conn.commit()
    conn.close()




@app.route("/")
def home():
    return render_template("index.html")

@app.route("/adoption")
def adoption():
    return render_template("adoption.html")

@app.route("/cart")
def cart():
    return render_template("cart.html")

@app.route("/clothing")
def clothing():
    return render_template("clothing.html")

@app.route("/food")
def food():
    return render_template("food.html")

@app.route("/products")
def product():
    return render_template("products.html")

@app.route("/toys")
def toys():
    return render_template("toys.html")

@app.route("/treats")
def treats():
    return render_template("treats.html")

@app.route("/vaccination")
def vaccination():
    return render_template("vaccination.html")

@app.route("/thankyou")
def thankyou():
    return render_template("thankyou.html")





# Login route
@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        email = request.form.get("email")
        password = request.form.get("password")

        # Check if the user exists
        conn = create_connection()
        cur = conn.cursor()
        cur.execute("SELECT * FROM users WHERE email = ? AND password = ?", (email, password))
        user = cur.fetchone()

        if user:
            return render_template("thankyou.html")
        else:
            return "Invalid credentials! <a href='/login'>Try again</a>"

    return render_template("login.html")



# Registration route
@app.route("/registration", methods=["GET", "POST"])
def registration():
    if request.method == "POST":
        full_name = request.form["full_name"]  # Get full_name from the form
        dog_name = request.form["dog_name"]      # Get dog_name from the form
        dog_breed = request.form["dog_breed"]    # Get dog_breed from the form
        email = request.form["email"]
        password = request.form["password"]
        confirm_password = request.form["Confirm_password"]

        if password != confirm_password:
            return "Passwords do not match. Please <a href='/registration'>Try again</a>."

        # Insert data into the database
        conn = create_connection()
        cur = conn.cursor()
        try:
            cur.execute("INSERT INTO users (full_name, dog_name, dog_breed, email, password) VALUES (?, ?, ?, ?, ?)", 
                        (full_name, dog_name, dog_breed, email, password))
            conn.commit()
            return redirect('/login')  # Redirect to login after successful registration
        except sqlite3.IntegrityError:
            return "Email already exists. Please <a href='/registration'>Try again</a>."
        finally:
            conn.close()

    return render_template("registration.html")



if __name__ == "__main__":
    create_table()
    app.run(debug=True)