import requests
import json
import webbrowser
import spotipy
import pytube
from spotipy.oauth2 import SpotifyOAuth

lz_uri = 'https://open.spotify.com/playlist/27TMze6OVbBfuq2bVqZTUK?si=84dd3ebb042a4eb7'
client_ID = "b574871f68ee4ace9789aa060670e5b7"
api_key= "AIzaSyDEcKW7J1eeH0Y42Tw_HmsB0oLPgDqscug"
query = "never+gonna+give+you+up+rick+astley"
searchquery = "https://www.googleapis.com/youtube/v3/search?part=snippet&maxResults=25&q=" + query + "&type=video&key=AIzaSyDEcKW7J1eeH0Y42Tw_HmsB0oLPgDqscug"

response = requests.get(searchquery)
data = response.json()
videoId = data['items'][0]['id']['videoId']
name = data['items'][0]['snippet']['title']
print(name)
print(videoId)
link = "https://www.youtube.com/watch?v=" + videoId
SAVE_PATH = "D:\TestingAutomationMusicDownloads"
  
video = pytube.YouTube(link)

video.streams.filter(progressive=True, file_extension='mp3').first().download(
output_path=SAVE_PATH, filename=name)
