import  requests
import urllib.parse


class SpotifyClient(object):

    def __init__(self, api_token):
        self.api_token = api_token

    def search_for_a_song(self, artist, track):

        query = urllib.parse.quote(f'{artist} {track}')
        url = f'https://api.spotify.com/v1/search?q={query}&type=track'

        response = requests.get(
            url,
            headers={
                'Content-Type': 'application/json',
                'Authorization': f'Bearer {self.api_token}'
            }
        )
        response_json  = response.json()
        print("in spotfy cleint , search for a song printing response json", response_json)
        results = response_json['tracks']['items']

        if results:
            return results[0]['id']

        else:
            raise Exception(f'Song not found for {artist} = {track}')

    def add_song_to_playlist(self, song_id):

        url = 'https://api.spotify.com/v1/me/tracks'

        response = requests.put(

            url,
            json = {
                'ids': [song_id]
            },
            headers = {
            'Content-Type': 'application/json',
            'Authorization': f'Bearer {self.api_token}'
        }
        )

        return response.ok