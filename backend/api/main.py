from flask import Flask, request
from utils.calculations import viability_score
# from utils.coordinate_getter import get_coordinates
# from utils.get_data import Datasets
# from backend.utils

app = Flask(__name__)


@app.route("/score")
def get_score():
    location = request.args.get('location')
    # Get the latitude and longitude of the address that was selected

    return f"<p>Calculated score for {location} is:  <i>{viability_score(location)}</i></p>"


if __name__ == "__main__" :
    app.run(debug=True)
