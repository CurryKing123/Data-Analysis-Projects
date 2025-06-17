import os
from googleapiclient.discovery import build
from dotenv import load_dotenv
import pandas as pd

load_dotenv()

api_key = os.getenv("api_key")
    
youtube = build('youtube', 'v3', developerKey=api_key)

def main():

    channel_ids = [os.getenv('channel_id'),
                   'UCUT8RoNBTJvwW1iErP6-b-A',
                   'UCfl_9KvN0Mjre_JmSDmbBlA',]

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
                'totalVideos': item['statistics']['videoCount'],
                'playlistId': item['contentDetails']['relatedPlaylists']['uploads']
                }
        all_data.append(data)

    print(pd.DataFrame(all_data))
    
def Most_Viewed_Video():

    playlist_ids = ['PLwYRiq-Ob29vrHcL-VVbxUdI2m-WdJpCM',]
    
    api_key = os.getenv("api_key")
    
    youtube = build('youtube', 'v3', developerKey=api_key)

    video_ids = []

    request = youtube.playlistItems().list(
        part = 'snippet,contentDetails',
        playlistId=','.join(playlist_ids),
        maxResults=50
    )

    response = request.execute()

    for item in response['items']:
        video_ids.append(item['contentDetails']['videoId'])

    #run requests for each page
    next_page_token = response.get('nextPageToken')

    while next_page_token is not None:
        request = youtube.playlistItems().list(
            part = 'snippet,contentDetails',
            playlistId=','.join(playlist_ids),
            maxResults = 50,
            pageToken = next_page_token,
        )

        response = request.execute()

        for item in response['items']:
            video_ids.append(item['contentDetails']['videoId'])

        #run requests for each page
        next_page_token = response.get('nextPageToken')

    print(len(video_ids))

    all_video_info = []

    request = youtube.videos().list(
        part='snippet,contentDetails,statistics',
        id = video_ids[0:5]
    )
    response = request.execute()

    for video in response['items']:
        data = {'snippet' : ['channelTitle', 'title', 'description', 'tags', 'publishedAt'],
                'statistics': ['viewCount', 'likeCount', 'favoriteCount', 'commentCount'],
                'contentDetails' : ['duration', 'definition', 'caption']}
    
        video_info = {}
        video_info['video_id'] = video['id']

        for k in data.keys():
            for v in data[k]:
                video_info[v] = video[k][v]
        
        all_video_info.append(video_info)

    print(all_video_info)