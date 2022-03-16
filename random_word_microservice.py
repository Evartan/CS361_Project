# This is the microservice provided to my teammate Jesse Zelaya

from flask import Flask
from random_word import RandomWords
r = RandomWords()

app = Flask(__name__)


@app.route("/")
def get_random_word():
    return r.get_random_word()


if __name__ == '__main__':
    app.run(debug=False)
