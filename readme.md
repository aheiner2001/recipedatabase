## Overview

**Project Title**: Personal Cookbook

**Project Description**:
Recipe Cookbook for possible future use with family

**Project Goals**:
- Enable users to create and store recipes with ingredient lists and cooking instructions.
- Allow users to update and delete their recipes.
- Provide a search feature for users to find recipes easily.
- Ensure security through user authentication and session management.
- Improve the user experience with a simple and intuitive interface.

## Instructions for Build and Use

### Steps to build and/or run the software:
1. Clone the repository from GitHub.
2. Install the necessary dependencies using `pip install -r requirements.txt`.
3. Set up a MySQL database and import the provided schema.
4. Configure the `config.py` file with the correct database credentials.
5. Run the application with `python app.py`.
6. Open a web browser and navigate to `http://localhost:5000` to access the application.

### Instructions for using the software:
1. Add a new recipe by providing a name, ingredients, and instructions.
2. View a list of your saved recipes on the home page.
3. Click on a recipe to view details 


## Development Environment

* Python 3.10+
* Flask 2.0+
* MySQL 8.0+
* mysql-connector-python
* Jinja2 for templating
* HTML, CSS, and JavaScript for frontend

## Useful Websites to Learn More

I found these websites useful in developing this software:

* [Flask Documentation](https://flask.palletsprojects.com/)
* [MySQL Documentation](https://dev.mysql.com/doc/)
* [Jinja2 Templating](https://jinja.palletsprojects.com/)

## Future Work

The following items I plan to fix, improve, and/or add to this project in the future:

* [ ] Implement the ability to edit only the name of a recipe.
* [ ] Improve the user interface with better styling and responsiveness.
* [ ] Enable image uploads for recipes.
* [ ] Implement an API for external integrations.
* [ ] Allow users to share recipes publicly or with friends.
* [ ] Add user preferences and dietary filters for recipe suggestions.
* [ ] Improve the database schema for better scalability and performance.
