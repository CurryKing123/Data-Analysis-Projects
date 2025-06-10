import requests
import json

base_url = "https://www.googleapis.com/youtube/v3/search"

parameters = {
    "part": "snippet",
    "forMine" : "true"
}
response = requests.get(base_url, params=parameters)
print(response)