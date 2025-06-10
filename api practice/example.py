import os

import google_auth_oauthlib.flow
from googleapiclient.discovery import build
import googleapiclient.errors

import api

def main():
    api_key = api.key
    
    youtube = build('youtube', 'v3', developerKey=api_key)

    # request = youtube.channels().list(
    #     part='statistics',
    #     forUsername='BBCNews'
    # )

    request = youtube.videos().list(
        part = 'statistics',
        chart = 'mostPopular'
    )

    response = request.execute()

    

if __name__ == "__main__":
    main()