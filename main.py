import requests
from datetime import datetime
import os

GENDER = "male"
AGE = "31"
HEIGHT = 178
WEIGHT_KG = 170
EXERCISE_ENDPOINT = "https://trackapi.nutritionix.com/v2/natural/exercise"

APP_ID = os.environ["NUTRITIONIX_APP_ID"]
API_KEY = os.environ["NUTRITIONIX_APP_KEY"]

SHEET_POST_ENDPOINT = os.environ["SHEET_ENDPOINT"]
USERNAME = os.environ["SHEET_USERNAME"]
PASSWORD = os.environ["SHEET_PASSWORD"]

params = {
    "query": input("Which exercises did you do today, and for how long? "),
    "gender": GENDER,
    "age": AGE,
    "weight_kg": WEIGHT_KG,
    "height_cm": HEIGHT
}

headers = {
    "x-app-id": APP_ID,
    "x-app-key": API_KEY
}

response = requests.post(url=EXERCISE_ENDPOINT, json=params, headers=headers)
data = response.json()

date_time = datetime.now()
today_date = date_time.strftime("%d/%m/%Y")
current_time = date_time.strftime("%H:%M:%S")

for exercise in data["exercises"]:
    my_workout = {
        "workout": {
            "date": today_date,
            "time": current_time,
            "exercise": exercise["name"].title(),
            "duration": exercise["duration_min"],
            "calories": exercise["nf_calories"]
        }
    }

    sheet_response = requests.post(url=SHEET_POST_ENDPOINT,
                                    json=my_workout,
                                    auth=(USERNAME, PASSWORD))
    print(sheet_response.text)

