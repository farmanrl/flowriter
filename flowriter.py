import sys
import json
import os
import lyricwikia
import markovify
import tweepy
import spotipy
from math import ceil
from textstat.textstat import textstat
from spotipy.oauth2 import SpotifyClientCredentials

logo = """==============================================================
\033[1m
    ___ _                   _
   / __) |                 (_)  _
 _| |__| | ___  _ _ _  ____ _ _| |_ _____  ____
(_   __) |/ _ \| | | |/ ___) (_   _) ___ |/ ___)
  | |  | | |_| | | | | |   | | | |_| ____| |
  |_|   \_)___/ \___/|_|   |_|  \__)_____)_|

By Richard Farman\033[0m
Built with \033[94mSpotipy\033[0m, \033[92mLyricsWikia\033[0m, \033[91mMarkovify\033[0m, and \033[93mTweepy\033[0m
=============================================================="""


SPOTIFY_ID = '9a9ec3dbfd0b43c2aeb707c252d5105b'
SPOTIFY_SECRET = '2306e2187d8847569ffba7cd75a8abc4'

client_credentials_manager = SpotifyClientCredentials(
    SPOTIFY_ID,
    SPOTIFY_SECRET
)

sp = spotipy.Spotify(client_credentials_manager=client_credentials_manager)

TWITTER_CONSUMER_KEY = 'DXdbE0wTlHxEFaGkv8RAlQuao'
TWITTER_CONSUMER_SECRET = '5ZLygS0lYZLByXhoChTItOn0C4M4We6VAYLM5CDPW8VfRtkHMx'
TWITTER_ACCESS_KEY = '854476066873683968-mhz3oInLa7pIJLGJiIyYLWDM0s96Zuk'
TWITTER_ACCESS_SECRET = 'tH4433OTMdBKb5LqXW54kzTVSIOn90bGdVVMi93PE7vXa'

auth = tweepy.OAuthHandler(TWITTER_CONSUMER_KEY, TWITTER_CONSUMER_SECRET)
auth.set_access_token(TWITTER_ACCESS_KEY, TWITTER_ACCESS_SECRET)

twitter = tweepy.API(auth)

# Return the most relevant artist object from a search of Spotify.
def get_artist(q):
    artist_results = sp.search(q, type='artist', limit=1)
    if len(artist_results['artists']['items']) > 0:
        artist = artist_results['artists']['items'][0]
    else:
        artist = None
    return artist


# Return a list of album IDs from an artist.
def get_artist_albums(artist_id):
    artist_album_results = sp.artist_albums(artist_id)
    artist_albums = artist_album_results['items']
    return artist_albums


# Return a list of tracks from a list of albums.
def get_album_tracks(artist_albums):
    tracks = []
    for album in artist_albums:
        album_id = album['id']
        album_tracks_results = sp.album_tracks(album_id)
        album_tracks = album_tracks_results['items']
        tracks += album_tracks
    return tracks


# Return lyrics for a track.
def get_lyrics(artists, track):
    for artist in artists:
        try:
            artist_name = artist['name']
            lyric = lyricwikia.get_lyrics(artist_name, track)
            lyric_lines = lyric.splitlines()
            return lyric_lines
        except Exception:
            continue


# Return a set of unique lyrics from an artist's tracks.
def get_artist_lyrics(artist_id):
    artist_albums = get_artist_albums(artist_id)
    print(len(artist_albums), 'albums found...')
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
    return newline_text


# Builds a markov model for an artist
def build_model(artist_id):
    print("Generating a new model, this may take awhile...")
    lyrics = get_artist_lyrics(artist_id)
    model = markovify.NewlineText(lyrics)
    write_model(model, artist_id)
    return model


# Writes a markov model to a file corresponding to artist ID.
def write_model(model, artist_id):
    model_json = model.to_json()
    file_name = os.path.join(sys.path[0], 'artists/' + artist_id + '.json')
    with open(file_name, 'w') as f:
        json.dump(model_json, f)


# Reades a markov model from a file corresponding to artist ID.
def read_model(file_name):
    with open(file_name, 'r') as f:
        model_json = json.load(f)
        model = markovify.NewlineText.from_json(
            model_json
        )
        return model


# Either loads a model from memory or builds one from scratch.
def get_model(artist_id):
    try:
        file_name = os.path.join(sys.path[0], 'artists/' + artist_id + '.json')
        model = read_model(file_name)
    except Exception:
        model = build_model(artist_id)
    return model


# Construct a haiku to the best of our ability from a markov model.
def make_haiku(model, artist_name):
    haiku_scheme = [5, 7, 5]
    char_limit = 140 - len(artist_name) - 3
    haiku_poem = [artist_name + ' - ']
    for h in haiku_scheme:
        while True:
            sentence = model.make_short_sentence(
                char_limit,
                max_overlap_total=3
            )
            if sentence:
                syllables = ceil(textstat.syllable_count(sentence))
                if syllables == h:
                    haiku_poem.append(sentence)
                    break
    haiku = '\n'.join(haiku_poem)
    return haiku


# Main control flow.
def main():
    print(logo)

    if len(sys.argv) > 1:
        q = sys.argv[1]
        artist = get_artist(q)
        if artist:
            print(artist)
            artist_id = artist['id']
            artist_name = artist['name']
    else:
        while True:
            print("Please enter an artist to model!")
            q = input('> ')
            if q:
                artist = get_artist(q)
                if artist:
                    artist_id = artist['id']
                    artist_name = artist['name']
                    break

    print("Artist", artist_name, "found, searching for lyrics")
    model = get_model(artist_id)
    print("Generating lyrics for you...")

    while True:
        haiku = make_haiku(model, artist_name)
        print("\033[1m" + haiku + "\033[0m")
        print(
            "Press any 't' to tweet, 'q' to quit, or any other key to continue"
        )
        response = input('> ')
        if response is 'q':
            sys.exit(1)
        elif response is 't':
            twitter.update_status(haiku)
        else:
            continue
    else:
        print("Please enter an artist to model!")


if __name__ == '__main__':
    main()
