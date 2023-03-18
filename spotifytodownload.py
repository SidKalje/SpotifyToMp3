from tkinter import * 
from tkinter import filedialog
from tkinter.filedialog import askdirectory
import tkinter as tk
from tkinter import messagebox
from tkinter import ttk, PhotoImage, Toplevel
import ttkbootstrap as tb
from threading import Thread
import threading
import requests
import json
import webbrowser
import spotipy
import pytube
from spotipy.oauth2 import SpotifyOAuth

class convertPythonToMp3():

    def __init__(self):
        self.playlistLink = None
        self.SAVE_PATH = None
        self.playlist = None
        self.client_ID = "b574871f68ee4ace9789aa060670e5b7"
        self.client_Secret = "da5f9db9a903435ca2baa9ea06f3452c"
        self.redirect_URI = "http://localhost:8888/callback"
        self.sp_oauth = SpotifyOAuth(client_id=self.client_ID, client_secret= self.client_Secret, redirect_uri= self.redirect_URI, scope="user-library-read")
        self.spotify = spotipy.Spotify(auth_manager= self.sp_oauth)
        self.run()

    def run(self):
        self.window=tb.Window(themename = "darkly")
        self.window.title('SpotifyToMp3')
        self.window.geometry('400x400')
        self.style = ttk.Style()
        self.style.configure(self.window, font = ("Ubuntu", 13))
        self.window.resizable(0,0)
        self.fileLoc = tb.Label(self.window, text = "File Location: Not Selected")
        self.fileLoc.pack(side = tk.TOP, pady = (30, 10))
        self.button = tb.Button(self.window, text = "Select Folder Location", command = self.openFile)
        self.button.pack(side = tk.TOP)
        self.playlistLabel = tb.Label(self.window, text = "Playlist Name: Not Selected")
        self.playlistLabel.pack(side = tk.TOP, pady = (50, 5))
        self.giveLink = tb.Text(self.window, height = 1)
        self.giveLink.pack(side = tk.TOP)
        self.acceptLink = tb.Button(self.window, text = "Accept Link", command = self.setPlaylistLink)
        self.acceptLink.pack(side = tk.TOP, pady = (5, 30))
        self.progress = tb.Label(self.window, text = "")
        self.progress.pack(side = tk.TOP, pady = (0, 3))
        self.convert = tb.Button(self.window, text = "Convert Playlist to MP3", command = self.convertSongs)
        self.convert.pack(side = tk.TOP, ipadx = 50, ipady = 20, pady = (20, 0))

        self.window.mainloop()

    def convertSongs(self):
        if(self.playlistLink == None):
            messagebox.showerror("Error", "Please enter a playlist link")
            return
        if(self.SAVE_PATH == None):
            messagebox.showerror("Error", "Please select a folder to save the files")
            return
        self.parsePlaylist()

    def openFile(self):
        newpath  = askdirectory(initialdir = "/", title = "Select Folder Location")
        if(newpath!="" and newpath!=self.SAVE_PATH):
            self.SAVE_PATH = newpath
            self.fileLoc.config(text = "File Location: " + self.SAVE_PATH)
            self.window.update()
    
    def setPlaylistLink(self):
        self.playlistLink = self.giveLink.get("1.0", "end-1c")
        try:
            self.playlist = self.spotify.playlist(self.playlistLink)
        except Exception as error:
            messagebox.showerror("Error", error)
            return
        results = self.spotify.user_playlist(user=None, playlist_id=self.playlistLink, fields="name")
        self.playlistName = results['name']
        self.playlistSongs = len(self.playlist['tracks']['items'])
        self.playlistLabel.config(text = "Playlist Name: " + self.playlist['name'] + ", " + str(len(self.playlist['tracks']['items'])) + " songs")
        self.window.update()
        #print(self.playlistLink)
        

    def findvidanddownload(self, query):
        api_key= "AIzaSyDEcKW7J1eeH0Y42Tw_HmsB0oLPgDqscug"
        searchquery = "https://www.googleapis.com/youtube/v3/search?part=snippet&maxResults=25&q=" + query + "&type=video&key=AIzaSyDEcKW7J1eeH0Y42Tw_HmsB0oLPgDqscug"

        response = requests.get(searchquery)
        data = response.json()
        videoId = data['items'][0]['id']['videoId']
        name = data['items'][0]['snippet']['title']
        #print(name)
        #print(videoId)
        link = "https://www.youtube.com/watch?v=" + videoId
        #print(link)
        video = pytube.YouTube(link)

        stream = video.streams.filter(only_audio=True).first().download(
        output_path=self.SAVE_PATH, filename=name+".mp3")


    

    #get all items in playlist using spotipy

    def parsePlaylist(self):
        numsongs = len(self.playlist['tracks']['items'])
        songsdone = 0
        self.progress.config(text = "Progress: " + str(songsdone) + "/" + str(numsongs))
        self.window.update()
        results = self.spotify.playlist_tracks(self.playlistLink)
        tracks = results['items']
        while results['next']:
            results = self.spotify.next(results)
            tracks.extend(results['items'])
        for track in tracks:
            #print(track['track']['name'] + " - " + track['track']['artists'][0]['name'])
            name = str(track['track']['name'])
            artist = str(track['track']['artists'][0]['name'])
            name = name.replace(" ", "+")
            artist = artist.replace(" ", "+")
            query = name + "+by+" + artist
            #print(query)
            self.findvidanddownload(query)
            songsdone = songsdone + 1
            self.progress.config(text = "Progress: " + str(songsdone) + "/" + str(numsongs))
            self.window.update()
            #print("done")
        messagebox.showinfo("Success", "Playlist has been converted to MP3")


convertPythonToMp3()