from flask import Flask, render_template, request
import requests

app = Flask(__name__)

API_KEY = "****"

@app.route("/", methods=["GET", "POST"])
def index():
    weather = None
    city = None  # define it upfront
    if request.method == "POST":
        city = request.form.get("city")
        if city:  # only proceed if city is provided
            city = city.strip().title()
            url = f"http://api.openweathermap.org/data/2.5/weather?q={city}&appid={API_KEY}&units=metric"
            response = requests.get(url)
            print(response.status_code, response.text)  # debug
            if response.status_code == 200:
                data = response.json()
                weather = {
                    "city": data["name"],
                    "temp": data["main"]["temp"],
                    "description": data["weather"][0]["description"].title(),
                    "icon": data["weather"][0]["icon"]
                }
            else:
                weather = {"error": "City not found!"}
        else:
            weather = {"error": "Please enter a city name!"}
    return render_template("index.html", weather=weather)

if __name__ == "__main__":
    app.run(debug=True)