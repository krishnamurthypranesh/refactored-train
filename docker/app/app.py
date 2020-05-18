import time

from flask import Flask, render_template, jsonify

app = Flask(__name__)

@app.route('/')
def homepage():
    return render_template('home.html')


@app.route('/time/', methods=['POST'])
def timetit():
    start = time.time()
    j = 0
    for i in range(1000):
        j += i ** i
    end = time.time()
    return jsonify({'time': end - start})
