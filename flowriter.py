import sys
import spotipy
import lyricwikia
import markovify
import json
from spotipy.oauth2 import SpotifyClientCredentials


CLIENT_ID = '9a9ec3dbfd0b43c2aeb707c252d5105b'
CLIENT_SECRET = '2306e2187d8847569ffba7cd75a8abc4'

client_credentials_manager = SpotifyClientCredentials(CLIENT_ID, CLIENT_SECRET)
sp = spotipy.Spotify(client_credentials_manager=client_credentials_manager)

genre_list = sp.recommendation_genre_seeds()


def get_artist(q):
    artist_results = sp.search(q, type='artist', limit=1)
    artist = artist_results['artists']['items'][0]
    return artist


def get_artist_albums(artist_id):
    artist_album_results = sp.artist_albums(artist_id)
    artist_albums = artist_album_results['items']
    return artist_albums


def get_album_tracks(artist_albums):
    tracks = []
    for album in artist_albums:
        album_id = album['id']
        album_tracks_results = sp.album_tracks(album_id)
        album_tracks = album_tracks_results['items']
        tracks += album_tracks
    return tracks


# def search_genre(q):
#     print("Recommending...")
#     seed_genres = [].append(q)
#     genre_results = sp.recommendations(seed_genres, limit=50)
#     tracks = genre_results['tracks']['items']
#     return tracks


def get_lyrics(artists, track):
    for artist in artists:
        try:
            artist_name = artist['name']
            lyric = lyricwikia.get_lyrics(artist_name, track)
            lyric_lines = lyric.splitlines()
            return lyric_lines
        except Exception:
            continue


def get_artist_lyrics(q):
    artist = get_artist(q)
    artist_id = artist['id']
    artist_name = artist['name']
    print(artist_name, 'found...')
    artist_id = artist['id']
    artist_albums = get_artist_albums(artist_id)
    print(len(artist_albums), 'artist albums found...')
    album_tracks = get_album_tracks(artist_albums)
    print(len(album_tracks), 'tracks found...')
    lyrics = []
    for track in album_tracks:
        artists = track['artists']
        name = track['name']
        lyric = get_lyrics(artists, name)
        if lyric:
            lyrics += lyric
    unique_lyrics = set(lyrics)
    newline_text = '\n'.join(unique_lyrics)
    return artist, newline_text


def get_model_from_web(q):
    print("Generating a new model, this may take awhile...")
    artist, lyrics = get_artist_lyrics(q)
    artist_id = artist['id']
    model = markovify.NewlineText(lyrics)
    model_json = model.to_json()
    file_name = artist_id + '.json'
    with open(file_name, 'w') as f:
        json.dump(model_json, f)
    return model


def get_model_from_file(file_name):
    with open(file_name, 'r') as f:
        model_json = json.load(f)
        model = markovify.NewlineText.from_json(
            model_json
        )
        return model


def get_model(q):
    try:
        artist_id = get_artist(q)['id']
        file_name = artist_id + '.json'
        model = get_model_from_file(file_name)
    except Exception:
        model = get_model_from_web(q)
    return model


def main():
    print("\033[1mWelcome to Flowriter v2.0\033[0m")
    if len(sys.argv) > 1:
        q = sys.argv[1]
    else:
        print("Please enter an artist to search and try again!")
        q = input('> ')
    model = get_model(q)
    if q:
        print("Generating lyrics for you...")
        while True:
            sentence = model.make_short_sentence(140)
            print("\033[1m" + sentence + "\033[0m")
            print("Press any key to continue, or 'q' to quit")
            response = input('> ')
            if response is 'q':
                sys.exit(1)
    else:
        print("Please enter an artist to search and try again!")


if __name__ == '__main__':
    main()
