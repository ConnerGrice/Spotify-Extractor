import spotipy
from spotipy.oauth2 import SpotifyOAuth
import cred
import SQLfuncs
import time

#list of scopes: https://developer.spotify.com/documentation/general/guides/authorization/scopes/#user-read-private
#list of methods: https://spotipy.readthedocs.io/en/master/#getting-started

#Returns a dict of all the songs on a playlist (regardless of limit)
def getTracks(playlistID):

    #Gets first 100 items from a playlist
    results = sp.playlist_items(playlistID)
    tracks = results['items']
    
    #Loops into it reaches the end of the playlist
    while results['next']:
        #Looks at the next 100 items in the playlist
        results = sp.next(results)
        #extends the list to include the extra items
        tracks.extend(results['items'])
    return tracks

def getImage(item,size):

    if len(item['images']) == 0:
        return "null","null","null"

    itemURL = item['images'][size]['url']
    itemH = item['images'][size]['height']
    itemW = item['images'][size]['width']

    return itemURL,itemH,itemW

#Dictates what methods can be used
scope= "playlist-read-private user-read-private"

#Connects to user account
sp = spotipy.Spotify(auth_manager=SpotifyOAuth(client_id=cred.clientID,client_secret=cred.clientSecret,redirect_uri=cred.redirectURL,scope=scope))

#Gets current users saved playlist info
playlists = sp.current_user_playlists()

#Establish connection to MySQL database
connection = SQLfuncs.dbConnection("localhost",cred.userName,cred.userPassword,"spotify")

#Deletes existing data
SQLfuncs.queryExecute(connection, "DELETE FROM Songs;")
SQLfuncs.queryExecute(connection, "DELETE FROM Albums;")
SQLfuncs.queryExecute(connection, "DELETE FROM Artists;")
SQLfuncs.queryExecute(connection, "DELETE FROM Playlists;")

#initialising lists to hold artist and album that appear in user playlists
artistIDs = []  
albumIDs = []

#Primary key counters
playlistPri = 1
counter = 1
#Loops though all of my playlists
for playlist in playlists['items']:

    #Gets a list of all the tracks in each playlist
    tracks = getTracks(playlist['id'])

    #Gets values to be placed in playlist database
    playlistName = playlist['name'] #Name of playlist
    playlistLength = len(tracks)    #Number of tracks in playlist
    playlistOwner = playlist['owner']['display_name']   #Name of playlist creator
    playlistImageURL,playlistImageH,playlistImageW = getImage(playlist,0)   #Gets image info
    
    #Bug fix for if image doesnt specify image dimensions
    if playlistImageH == None or playlistImageW == None:
        playlistImageH = "null"
        playlistImageW = "null" 

    #Adding data to database
    query = f"""
    INSERT INTO Playlists VALUES
    ({playlistPri},"{playlistName}",{playlistLength},"{playlistOwner}","{playlistImageURL}",{playlistImageH},{playlistImageW});
    """
    SQLfuncs.queryExecute(connection,query)

    #Loops though all the tracks in the track list
    for track in tracks:
        #Generates list of all artists and albums in all playlists
        artistIDs.append(track['track']['artists'][0]['id'])
        albumIDs.append(track['track']['album']['id'])

        print(f"SCANNING TRACK {counter} from {playlistName}: {track['track']['name']}")

        counter += 1
    playlistPri += 1

print("SCANNING COMPLETE! - Ordering artists and playlists")
#Remove duplicates
artsClean = list(dict.fromkeys(artistIDs))
albsClean = list(dict.fromkeys(albumIDs))

#Number of unique artists and albums in all playlists
artsLen = len(artsClean)
albsLen = len(albsClean)

print("RECORDING ARTIST INFO")
#Primary key for artists
artistID = 1

#Loops through all artists and records info
for artist in artsClean:

    #Gets specific artist info
    artistFull = sp.artist(artist)

    #Gets attributes
    artistName = artistFull['name']
    artistGenres = artistFull['genres']
    artistImageURL,artistImageH,artistImageW = getImage(artistFull,0)

    #Adding data to data base
    query = f"""INSERT INTO Artists VALUES
    ({artistID},"{artistName}","{artistGenres}","{artistImageURL}",{artistImageH},{artistImageW});
    """
    SQLfuncs.queryExecute(connection,query)

    print(f"PROCESSING ARTIST {artistID}/{artsLen}: {artistName}")

    artistID += 1


print("RECORDING ALBUM INFO")
#Primary key for albums
albumPri = 1

#Loops though all albums and records info 
for album in albsClean:
    #Gets specific album data
    albumFull = sp.album(album)

    #Gets attributes
    albumName = albumFull['name']
    albumImageURL,albumImageH,albumImageW = getImage(albumFull,0)

    #Finds which artist the album belongs to and sets the foreign key
    for i in range(artsLen):
        if albumFull['artists'][0]['id'] == artsClean[i]:
            artistPri = i + 1

    #Adds data to database
    query = f"""INSERT INTO Albums VALUES
    ({albumPri},"{albumName}","{albumImageURL}",{albumImageH},{albumImageW},{artistPri});
    """
    SQLfuncs.queryExecute(connection,query)

    print(f"PROCESSING ALBUM {albumPri}/{albsLen}: {albumName}")

    albumPri += 1


print("RECORDING SONG INFO")

#Primary key for songs
songPri = 1
playlistPri = 1
#Loops though all playlists
for playlist in playlists['items']:

    #Gets a list of all the tracks in each playlist
    tracks = getTracks(playlist['id'])

    #Loops though all tracks in each playlist
    for track in tracks:

        #Checks for artist of track
        for i in range(len(artsClean)):
            if track['track']['artists'][0]['id'] == artsClean[i]:
                #Input artistID
                artistPri = i + 1

        #Checks for album of track
        for i in range(len(albsClean)):
            if track['track']['album']['id'] == albsClean[i]:
                #Input albumID
                albumPri = i + 1

        #Gets specific track audio features info
        trackInfo = sp.audio_features(track['track']['id'])

        #Gets attributes
        trackName = track['track']['name']
        trackDuration = track['track']['duration_ms']
        trackDance = trackInfo[0]['danceability']
        trackTempo = trackInfo[0]['tempo']
        trackEnergy = trackInfo[0]['energy']

        #Adds data to database
        query = f"""INSERT INTO Songs VALUES
        ({songPri},"{trackName}",{playlistPri},{trackDuration},{trackDance},{trackTempo},{trackEnergy},{artistPri},{albumPri});
        """
        SQLfuncs.queryExecute(connection,query)

        print(f"PROCESSING TRACK {songPri}/{counter} from {playlist['name']}: {trackName}")

        songPri += 1

    playlistPri += 1
