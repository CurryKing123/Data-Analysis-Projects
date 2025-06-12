import os
from googleapiclient.discovery import build
from dotenv import load_dotenv
import pandas as pd

def main():

    load_dotenv()

    channel_ids = [os.getenv('channel_id'),]
    
    api_key = os.getenv("api_key")
    
    youtube = build('youtube', 'v3', developerKey=api_key)

    # request = youtube.channels().list(
    #     part='statistics',
    #     forUsername='BBCNews'
    # )

    all_data = []

    request = youtube.channels().list(
        part = 'snippet,contentDetails,statistics',
        id=','.join(channel_ids)
    )

    response = request.execute()
    print (response)
    
    for item in response['items']:
        data = {'channelName': item['snippet']['title'],
                'subscribers': item['statistics']['subscriberCount'],
                'views': item['statistics']['viewCount'],
                'totalViews': item['statistics']['videoCount'],
                'playlistId': item['contentDetails']['relatedPlaylists']['uploads']
                }
        all_data.append(data)

    print(pd.DataFrame(all_data))

    

if __name__ == "__main__":
    main()