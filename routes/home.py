from flask import Blueprint, render_template
from forms import CourseForm

home = Blueprint('home', __name__, url_prefix='/')


@home.route('/', methods=['GET'])
def index():
    form = CourseForm()
    return render_template('index.html', form=form)
