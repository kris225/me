import requests
from flask import Flask, request, render_template
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By


# Flask

app = Flask(__name__)


@app.route('/')
def home():
    return render_template("home.html")


@app.route('/about')
def about():
    return render_template("about.html")


hourly = {}
# OOPS
@app.route('/weather', methods=["GET", "POST"])
def weather():
    # APIs: gets current location, temperature in celsius and current condition

    API_Endpoint = "https://api.weatherapi.com/v1/forecast.json"
    API_Key = "d7096fdac7eb45f389135256222006"
    msg_a = "this location does not exist. try again. "
    msg_b = "(or u messed the spelling up :p)"

    if request.method == "POST":
        city = request.form.get("city")
        weather_params = {
            "key": API_Key,
            "q": city,
            "days": 1,
            "aqi": "no",
            "alerts": "no"
        }

        response = requests.get(API_Endpoint, params=weather_params)
        if response.status_code == 400:
            return render_template("weather-app/weather.html", msg_a=msg_a, msg_b=msg_b)
        weather_data = response.json()

        location = weather_data["location"]["name"]
        location = location.strip()
        current_temp = weather_data["current"]["temp_c"]
        current_condition = weather_data["current"]["condition"]["text"]

        times = weather_data["forecast"]["forecastday"][0]["hour"]
        # hourly_time = times[i]["time"]
        # hourly_condition = times[i]["condition"]["text"]
        global hourly
        hourly = {times[i]["time"][11:13]: times[i]["condition"]["text"] for i in range(0, len(times))}

        return render_template("weather-app/response.html", location=location.lower(), temp=current_temp,
                               condition=current_condition.lower(), hourly=hourly)
    return render_template("weather-app/weather.html")


@app.route('/more')
def more_info():
    return render_template("weather-app/more-info.html", hourly=hourly)


@app.route('/my-stats', methods=['GET', 'POST'])
def stats():
    pass


if __name__ == "__main__":
    app.run(debug=True)
