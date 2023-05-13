import requests


def get_coordinates(address):
    """This function gets the coordinates of a given address

    Args:
        address (str): The required address

    Returns:
        lat, lon: The lattitude and longitude of the given address
    """

    # Define the base URL for the Nominatim API
    url = "https://nominatim.openstreetmap.org/search"

    def contact_api(address):
        # Define the parameters for the API request
        params = {"q": address, "format": "jsonv2"}

        # Send the API request and get the response
        response = requests.get(url, params=params).json()

        # Go up a level if coordinates not found
        if len(response) == 0:
            trimmed_address = ",".join(address.split(",")[1:])
            response = contact_api(trimmed_address)

        return response

    response = contact_api(address)

    # Extract the latitude and longitude from the response
    lat = response[0]["lat"]
    lon = response[0]["lon"]

    return lat, lon
