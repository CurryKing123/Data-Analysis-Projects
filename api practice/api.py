import requests
import json
import sys
import os
import example

#grabbing api data from private folder outside of project
file_dir = os.path.join(os.path.dirname(__file__), '..', '..', 'API', 'Youtube')
sys.path.append(file_dir)


import youtube_api

#grab api key and client id from outside folder
key = youtube_api.key
client_id = youtube_api.client_id
client_secret = os.path.join(file_dir, 'client_secret.json')