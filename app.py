from flask import Flask, render_template, request, redirect, url_for, session
import os
from dotenv import load_dotenv
import mysql.connector
from werkzeug.security import generate_password_hash

app = Flask(__name__)

app.secret_key = "my$uper$ecureKey123!"
# Load environment variables
load_dotenv()

# Database connection
db = mysql.connector.connect(
    host=os.getenv('DB_HOST'),
    user=os.getenv('DB_USER'),
    password=os.getenv('DB_PASSWORD'),
    database=os.getenv('DB_NAME')
)

@app.route('/login')
def login():
 
    return render_template('login.html')



@app.route('/')
def home():
    # if 'user_id' not in session:
    #     return redirect('/login')
    # user_id = session['user_id'] 
    # user_id ="25" # Retrieve user ID from session

    
    cursor = db.cursor()
    cursor.execute("SELECT DISTINCT recipe_name,idrecipes from recipes")
    recipes = cursor.fetchall()

    # cursor = db.cursor()
    # cursor.execute("SELECT DISTINCT recipe_name,idrecipes from recipes WHERE users_idusers = %s", (user_id,))
    # recipes = cursor.fetchall()

    cursor.execute("SELECT ingredient_name,quantity,measurement_type, recipes_idrecipes from ingredients")
    ingredients = cursor.fetchall()

    cursor.execute("SELECT description, recipes_idrecipes from instructions")
    steps = cursor.fetchall()
    cursor.close()


    # cursor.execute("SELECT ingredient_name,quantity,measurement_type, recipes_idrecipes from ingredients WHERE recipes_idrecipes= %s", (user_id,))
    # ingredients = cursor.fetchall()

    # cursor.execute("SELECT description, recipes_idrecipes from instructions WHERE recipes_idrecipes= %s", (user_id,))
    # steps = cursor.fetchall()
    # cursor.close()

    return render_template('index.html', ingredients=ingredients, recipes=recipes, steps=steps)



@app.route('/add')
def add():
    return render_template("add_recipe.html")

@app.route('/register')
def register():
    return render_template("register.html")

@app.route('/register_user', methods=['POST'])
def register_user():
    user_name = request.form.get('username')
    key = request.form.get('key')
    # Hash the password

    cursor = db.cursor()
    cursor.execute("INSERT INTO users (user_name, user_password) VALUES (%s, %s)", (user_name, key))
    db.commit()
    cursor.close()
    return redirect('/')

@app.route('/login_user', methods=['POST', 'GET'])
def login_user():
    user_name = request.form.get('username')
    key = request.form.get('key')
    
    print(f"Username: {user_name}, Password: {key}")

    cursor = db.cursor()
    cursor.execute("SELECT idusers FROM users WHERE user_name = %s AND user_password = %s", (user_name, key))
    user = cursor.fetchall()
    cursor.close()
    if user:
        session['user_id'] = user[0]  # Store user_id in session
        return redirect('/')
    else:
        return "Invalid username or password", 401 

@app.route('/submit_recipe', methods=['POST'])
def add_recipe():


    cursor = db.cursor()
    recipe_name = request.form.get('recipe_name')
    serving_size = request.form.get('serving_size')
    user_id = session.get('user_id')

    cursor.execute("INSERT INTO recipes (recipe_name, serving_size, users_idusers) VALUES (%s, %s, %s)", 
                   (recipe_name, serving_size, user_id))
    

    ingredients = request.form.getlist('ingredients[]')
    units = request.form.getlist('units[]')
    quantities = request.form.getlist('quantities[]')
    meal_id = cursor.lastrowid


    for ingredient, unit, quantity in zip(ingredients, units, quantities):
        cursor.execute("INSERT INTO ingredients (ingredient_name, quantity, measurement_type, recipes_idrecipes) VALUES (%s, %s, %s, %s)", 
                   (ingredient, quantity, unit, meal_id))
   
    steps = request.form.getlist('directions[]')
    step_number = 1
    for step in steps:
        cursor.execute("INSERT INTO instructions (description,step_number, recipes_idrecipes) VALUES (%s, %s, %s)", 
                   (step, step_number, meal_id))
    


    # cursor.execute("INSERT INTO ingredients (recipe_name, serving_size, users_idusers) VALUES (%s, %s, %s)", 
    #                (recipe_name, serving_size,users_id))
   
    

    db.commit()
    cursor.close()

    return redirect('/')





@app.route('/recipe-details')
def recipe_details():
    recipe_id = request.args.get('recipe_id')  # Get the recipe ID from the URL
    # Fetch recipe details from the database using recipe_id
    cursor = db.cursor()

    recipe_name_query = "SELECT recipe_name, idrecipes from recipes WHERE idrecipes = %s"
    cursor.execute(recipe_name_query, (recipe_id,))
    recipes = cursor.fetchone() 


   
    ingredients_query = "SELECT ingredient_name,quantity,measurement_type, recipes_idrecipes from ingredients  WHERE recipes_idrecipes = %s"
    cursor.execute(ingredients_query, (recipe_id,))
    ingredients = cursor.fetchall()

   
    steps_query = "SELECT description from instructions WHERE recipes_idrecipes = %s"
    cursor.execute(steps_query, (recipe_id,))
    steps = cursor.fetchall()


    return render_template('display_recipie.html', ingredients=ingredients, recipes=recipes, steps=steps)
   






@app.route('/delete', methods=['POST'])
def delete_recipe():
    # recipe_id = request.form.get('id')
    # cursor = db.cursor()
    # cursor.execute("DELETE FROM recipes WHERE idrecipes = %s", (recipe_id,))
    # db.commit()
    # cursor.close()
    # return redirect('/')
    pass


    # cursor = db.cursor()
    # cursor.execute("SELECT recipe_name FROM recipes WHERE idrecipes = %s", (id,))
    # recipe = cursor.fetchone()

    # cursor.execute("SELECT ingredient_name, quantity, measurement_type FROM ingredients WHERE recipes_idrecipes = %s", (id,))
    # ingredients = cursor.fetchall()

    # cursor.execute("SELECT step_number, description FROM instructions WHERE recipes_idrecipes = %s ORDER BY step_number", (id,))
    # instructions = cursor.fetchall()

    # cursor.close()
    # return render_template('recipe_details.html', recipe=recipe, ingredients=ingredients, instructions=instructions)
    

if __name__ == '__main__':
    app.run(debug=True)
