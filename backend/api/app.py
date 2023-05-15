from flask import Flask

app = Flask(__name__)

@app.route("/score")
def get_score():
    return "<p>This should return calculated scores</p>"

