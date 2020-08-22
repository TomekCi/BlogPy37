from flask import app, render_template, request, redirect, Blueprint


example_blueprint = Blueprint('example_blueprint', __name__, template_folder='templates')



@example_blueprint.route('/2')
def index():
    # return "This is an example app"
    return render_template('index.html')

# @app.route('/home')
# @app.route('/index')

"""

"""