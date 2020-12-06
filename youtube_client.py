import os

import google_auth_oauthlib.flow
import googleapiclient.discovery
import googleapiclient.errors
import youtube_dl


class Playlist(object):

    def __init__(self, id, title):

        self.id = id
        self.title = title


class Song(object):

    def __init__(self, song, artist):
        self.artist = artist
        self.song = song

class YoutubeClient(object):

    def __init__(self, credentials_location):
        # -*- coding: utf-8 -*-
        print('cleint_location', credentials_location)
        # Sample Python code for youtube.playlists.list
        # See instructions for running these code samples locally:
        # https://developers.google.com/explorer-help/guides/code_samples#python

        scopes = ["https://www.googleapis.com/auth/youtube.readonly"]

        # Disable OAuthlib's HTTPS verification when running locally.
        # *DO NOT* leave this option enabled in production.
        os.environ["OAUTHLIB_INSECURE_TRANSPORT"] = "1"

        api_service_name = "youtube"
        api_version = "v3"

        # Get credentials and create an API client
        flow = google_auth_oauthlib.flow.InstalledAppFlow.from_client_secrets_file(
            credentials_location, scopes)
        credentials = flow.run_console()
        youtube_client = googleapiclient.discovery.build(
            api_service_name, api_version, credentials=credentials)
        print("returnfing")
        self.youtube_client  = youtube_client
    def get_playlists(self):

        request = self.youtube_client.playlists().list(
            part="snippet, contentDetails ",
            mine=True,
            maxResults=50
        )
        reponse = request.execute()
        playlists = [Playlist(item['id'], item['snippet']['title']) for item in reponse['items']]

        return playlists

    def get_vids_from_playlists(self, playlist_id):
        songs = []
        request = self.youtube_client.playlistItems().list(
            playlistId = playlist_id,
            part="id, snippet"
        )
        response = request.execute()

        for item in response['items']:
            video_id = item['snippet']['resourceId']['videoId']
            artist , track = self.get_artist_track_from_vid(video_id)

            if artist and track :
                songs.append(Song(artist, track))

        return songs

    #  youtube dl_library
    def get_artist_track_from_vid(self, vid_id):

        print("vid", vid_id)
        youtube_url = f'https://youtube.com/watch?v={vid_id}'

        try:
            video = youtube_dl.YoutubeDL({'quiet':True}).extract_info(youtube_url,download=False)

            print('vid details', video)
            artist = video['artist']
            track = video['track']
            return artist, track

        except Exception as e:
            print("no info available for this vid id", vid_id )






