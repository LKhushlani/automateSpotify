import os
from youtube_client import YoutubeClient
from spotify_client import SpotifyClient


def run():

    youtube_client = YoutubeClient('./creds/client_secret.json')
    spotify_client = SpotifyClient(os.getenv('SPOTIFY_AUTH_TOKEN'))
    playlists = youtube_client.get_playlists()

    # ask which playlist we want to get music vids from
    for index, playlist in enumerate(playlists):
        print(f'{index} : {playlist.title}')


    choice   = int(input('Please select the playlist  want to get music vids from'))
    chosen_playlist = playlists[choice]
    print("You chose : ", chosen_playlist.title)

    # for each playlist get the songs info from youtube
    songs = youtube_client.get_vids_from_playlists(chosen_playlist.id)
    print(f'trying to add {len(songs)}')

    # search for a song in spotify if found add it to the playlist
    for song in songs:
        spotify_song_id = spotify_client.search_for_a_song(song.artist, song.track)
        if spotify_song_id:
            added_song = spotify_client.add_song_to_playlist(spotify_song_id)
            if added_song:
                print(f'{song.track} added successfully !! ')

            else:
                print("sorry could not add song : ( ")

        else:
            print("song not found on Spotify :( ")

    # add




if __name__ == '__main__':
    run()