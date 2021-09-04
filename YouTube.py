import os
import requests
import youtube_dl
from googleapiclient.discovery import build

api_key = '' # API key from Google Console
search_token = '' # search token to find track on Spotify
playlist_id = ''  # PLaylist ID
all_song_info = {}  # nested dictionary for all song information

youtube = build('youtube','v3',developerKey=api_key)

def get_spotify_uri(song_name,artist):
    query ="https://api.spotify.com/v1/search?query=track%3A{}+artist%3A{}&type=track&offset=0&limit=20".format(song_name,artist)
    response = requests.get(query,headers={
        "Content-Type":"application/json","Authorization": "Bearer {}".format(search_token)

    })
    response_json = response.json()
    songs = response_json["tracks"]["items"]
    #only use the first song
    try:
        uri = songs[0]["uri"]
    except IndexError:
        uri = 'null'
    return uri

def youtube_initiate():
    nextPageToken = None
    while True:
        pl_request = youtube.playlistItems().list(
            part='content Details',playlistId=playlist_id,maxResults=50,pageToken=nextPageToken
        )
        pl_response = pl_request.execute()
        nextPageToken =pl_response.get('nextPageToken')
        vid_ids = []
        # to iterate over every video in the playlist and get the ID.
        for item in pl_response['items']:
            vid_ids.append(item['contentDetails']['videoId'])
        vid_request = youtube.videos().list(
            part="snippet",id=",".join(vid_ids)
        )
        vid_response = vid_request.execute()
        # save video title, youtube URL
        for item in vid_response["items"]:
            video_title = item["snippet"]["title"]
            print (video_title)
            youtube_url = "https://www.youtube.com/watch?v={}".format(item["id"])
            #use youtube_dl to collect the song_name and artist name
            video = youtube_dl.YoutubeDL({}).extract_info(youtube_url,download=False)
            try:
                #extract the track name, artist and the spotify uri and save them in our dict
                song_name = video["track"]
                print(song_name)
                artist = video["artist"]
                print(artist)
                spotify_uri = get_spotify_uri(song_name,artist)
                #song information is added if exists
                if(spotify_uri!='null'):
                    all_song_info[video_title] = {"youtube_url": youtube_url, "song_name": song_name, "spotify_uri": spotify_uri}
            except KeyError as e:
                print("Current song details are unavailable ")
        if not nextPageToken:
            break
    print(len(all_song_info))
    print(all_song_info)
    return all_song_info