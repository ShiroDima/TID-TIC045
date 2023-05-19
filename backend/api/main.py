import calculations as calc
from flask import Flask, request
# import calculations here. Also fix imports in the calculation file itself.
import sys
sys.path.append('./utils')
# from utils.coordinate_getter import get_coordinates
# from utils.get_data import Datasets
# from backend.utils

app = Flask(__name__)


@app.route("/score")
def get_score():
    location = request.args.get('location')
    # Get the latitude and longitude of the address that was selected
    print(location)
    return f"<p>Calculated score for {location} is:  <i>{calc.viability_score(location)}</i></p>"


if __name__ == "__main__":
    app.run(debug=True)
