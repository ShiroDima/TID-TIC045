from flask import Flask, request

app = Flask(__name__)

@app.route("/score")
def get_score():
    location = request.args.get('location')
    # do a bunch of stuff here
    return f"<p>This should return calculated scores, for location = <i>{location}</i></p>"

if __name__ == "__main__" :
    app.run(debug=True)