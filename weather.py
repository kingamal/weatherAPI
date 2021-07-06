import requests
import sys
import json
from datetime import datetime, date, timedelta
from os.path import getmtime, exists


class Weather:
    def __init__(self):
        self.response = []

    def get_response(self, key):
        url = "https://community-open-weather-map.p.rapidapi.com/forecast"
        querystring = {"q":"san francisco,us"}
        headers = {
            'x-rapidapi-key': key,
            'x-rapidapi-host': "community-open-weather-map.p.rapidapi.com"
            }
        self.response = requests.request("GET", url, headers=headers, params=querystring).json()
        # print(self.response)

    def load_response(self, key, file):
        if not exists(file):
            self.get_response(key)
            self.save_response(file)
        sec = getmtime(file)
        now = datetime.now().timestamp()
        if now - sec < 60 * 60:
            with open(file, "r+") as f:
                self.response = json.load(f)
        else:
            self.get_response(key)
            self.save_response(file)

    def save_response(self, file):
        with open(file, 'w') as fp:
            file_content_json = json.dumps(self.response)
            fp.write(file_content_json)
        return True

    def forecast(self):
        what_weather = {}
        for day in self.response["list"]:
            date = datetime.utcfromtimestamp(day["dt"]).strftime("%Y-%m-%d") #unixtime
            forecast = day["weather"][0]["main"]
            what_weather[date] = forecast
        return what_weather


weather = Weather()
key = input()
outfile = sys.argv[1]
weather.load_response(key, outfile)
dictionary = weather.forecast()
if len(sys.argv) < 3:
    tomorrow = date.today() + timedelta(days=1)
    tomorrow = tomorrow.strftime("%Y-%m-%d")
    if tomorrow not in dictionary:
        print('Nie wiem')
    elif dictionary[tomorrow] == 'Rain' or dictionary[tomorrow] == 'Snow':
        print('Bedzie padac')
    else:
        print('Nie bedzie padac')
elif sys.argv[2] in dictionary:
    if dictionary[sys.argv[2]] == 'Rain' or dictionary[sys.argv[2]] == 'Snow':
        print('Bedzie padac')
    else:
        print('Nie bedzie padac')
else:
    print('Nie wiem')
