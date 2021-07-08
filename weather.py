import requests
import sys
import json
from datetime import datetime, date, timedelta
from os.path import getmtime, exists


class Weather:
    def __init__(self):
        self.response = []
        self.what_weather = {}
        self.counter = 0

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
            return
        sec = getmtime(file)
        now = datetime.now().timestamp()
        if now - sec < 60 * 60 * 24:
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
        for day in self.response["list"]:
            date = datetime.utcfromtimestamp(day["dt"]).strftime("%Y-%m-%d") #unixtime
            forecast = day["weather"][0]["main"]
            self.what_weather[date] = forecast
        return self.what_weather

    def __getitem__(self, item):
        if item not in self.what_weather:
            return 'Nie wiem'
        if 'Rain' in self.what_weather[item]:
            return 'Bedzie padac'
        elif 'Snow' in self.what_weather[item]:
            return 'Bedzie padac'
        else:
            return 'Nie bedzie padac'

    def items(self):
        return self.what_weather.items()

    def __iter__(self):
        self.counter = 0
        return self

    def __next__(self):
        if len(self.what_weather) <= self.counter:
            raise StopIteration
        what_date = list(self.what_weather.keys())[self.counter]
        self.counter += 1
        return what_date

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


print(weather['2021-07-08'])
print(weather.items())
for w in weather:
    print(w)