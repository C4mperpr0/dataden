from flask import *
from time import time
from math import floor
from random import seed, random

color_of_the_day = Blueprint("color_of_the_day", __name__, static_folder="static", template_folder="templates")


@color_of_the_day.route('/', methods=['GET', 'POST'])
def color_of_the_day_():
    seed(floor(time()/86400))
    color = [round(random()*255), round(random()*255), round(random()*255)]
    color_font = [(255-c) for c in color]
    return render_template('color_of_the_day.html',
                           color=f"#{''.join([hex(c)[2:] for c in color])}",
                           color_font=f"#{''.join([hex(c)[2:] for c in color_font])}")