from flask import Flask, render_template
import os
import json
import time
import urllib

APPID = "b8142d04c88945f7974103342dcc823b"

app = Flask(__name__)

def get_weather():
    url = "http://api.openweathermap.org/data/2.5/forecast/daily?q=Bucharest&cnt=10&mode=json&units=metric&APPID={}".format(APPID)
    return urllib.request.urlopen(url).read()

@app.route("/")
def index():
    data=json.loads(get_weather())
    page = "html<head><title>My Weather</title></head><body>"
    page += "<h1 Weather for {}, {}</h1>".format(data.get('city').get('name'), data.get('city').get('country'))
    for day in data.get('list'):
        page += "<b>date:</b><b>min:</b><b>max:</b><b>description:</b> {} <br /> ".format(
            time.strftime('%d %B', time.localtime(day.get('dt'))),
            (day.get("temp").get("min")),
            day.get("temp").get("max"),
            day.get("weather")[0].get("description")
        )
    page += "</body></html"
    return page

@app.route("/goodbye")
def goodbye():
    return "Goodbye, World"

@app.route("/hello/<name>/<int:age>")
def hello_name(name, age):
    return "Hello, {}, you are {} years old".format(name, age)

if __name__ == '__main__':
    port = int(os.environ.get('PORT',5000))
    app.run(host='0.0.0.0', port=port, debug=True)