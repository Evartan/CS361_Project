from flask import Flask, render_template, redirect, send_file, url_for
from forms import CourseForm
import json
import os
import pdfkit
import time

app = Flask(__name__)
app.config['SECRET_KEY'] = 'your secret key'

results_list = []


@app.route('/', methods=('GET', 'POST'))
def index():
    form = CourseForm()
    if form.validate_on_submit():
        # instad of appending to results we need to create a file with json data
        # saving data to json format
        json_data = {'ticker': form.ticker.data,
                     'date': form.date.data,
                     }
        json_dump = json.dumps(json_data, default=str)
        # creating file with json object
        with open("send.txt", "w+") as file:
            data = json_dump
            file.write(data)

        with open("run.txt", "w+") as r:
            r.write('run')

        # sleep 3 second
        time.sleep(3)

        # if the file exists, open it checking for "run"
        with open("data.txt", "r+") as file:
            data = file.read()

            if data == 'not found':
                return redirect(url_for('not_found'))

            data_dict = json.loads(data)
            results_list.insert(0, data_dict)

        return redirect(url_for('results'))
    return render_template('index.html', form=form)


@app.route('/results/')
def results():
    return render_template('results.html', results_list=results_list)


@app.route('/download')
def download_file():
    pdfkit.from_url('http://127.0.0.1:5000/results/', 'results.pdf')
    return send_file('results.pdf', as_attachment=True)


@app.route('/not_found/')
def not_found():
    return render_template('notfound.html')
