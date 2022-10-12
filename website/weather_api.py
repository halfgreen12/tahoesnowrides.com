import requests


def main(city_input):
    # result = ""
    api_key = "25c740a38cb7334ce07634b493b12e76"

    base_url = "http://api.openweathermap.org/data/2.5/weather?appid=" + api_key + "&q=" + city_input

    api_link = requests.get(base_url)

    # if api_data["cod"] == 200:
    try:
        api_data = api_link.json()
        temperature = api_data['main']["temp"]
        if temperature <= 290:
            result = f"{city_input} is a good place to snowboard!"
        else:
            result = f"It's too hot to snowboard in {city_input}."
    except Exception as err:
        error_string = str(err)
        print(error_string)
        result = "Please enter a valid city."
    return result
