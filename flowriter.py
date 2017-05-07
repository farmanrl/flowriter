import markovify
import urllib.request
import json
import lyricwikia
import sys

logo = """==============================================================
\033[1m
    ___ _                   _
   / __) |                 (_)  _
 _| |__| | ___  _ _ _  ____ _ _| |_ _____  ____
(_   __) |/ _ \| | | |/ ___) (_   _) ___ |/ ___)
  | |  | | |_| | | | | |   | | | |_| ____| |
  |_|   \_)___/ \___/|_|   |_|  \__)_____)_|


By Richard Farman\033[0m
Written in \033[93mPython3\033[0m with \033[94mMusicGraph\033[0m, \033[92mlyricswikia\033[0m, and \033[91mmarkovify\033[0m
=============================================================="""

api_key = None

try:
    f = open('API_KEY', 'r')
    api_key = f.read().replace('\n', '')
except:
    pass

genres = """Alternative/Indie
Blues
Cast Recordings/Cabaret
Christian/Gospel
Children's
Classical/Opera
Comedy/Spoken Word
Country
Electronica/Dance
Folk
Instrumental
Jazz
Latin
New Age
Pop
Rap/Hip Hop
Reggae/Ska
Rock
Seasonal
Soul/R&B
Soundtracks
Vocals
World""".lower().rstrip().replace(' ', '+').split('\n')

decades = """1890s
1900s
1910s
1920s
1930s
1940s
1950s
1960s
1970s
1980s
1990s
2000s
2010s
""".rstrip().split('\n')

yes_words = ['y', 'ye', 'yea', 'yee', 'yes', 'yeah', 'yup']
no_words = ['n', 'no', 'nop', 'nope', 'nah', 'nay']

model_types = ['artist', 'album', 'genres', 'decades']


def get_model_type():
    while True:
        print("\033[1mWould you like to model by artist, album, genres, or decades?\033[0m")
        model_type = input('> ').lower().rstrip()
        if model_type in model_types:
            break
#        if model == 'track':
#            base = 'http://api.musicgraph.com/api/v2/track/'
#            break
    return model_type


def get_tag(model_type):
    valid = True
    while valid:
        print("\033[1mEnter the name of the", model_type, "that you would like to model:\033[0m")
        if model_type == 'genres':
            print(genres)
        elif model_type == 'decades':
            print(decades)
        tag = input('> ').lower().rstrip().replace(' ', '+')
        if model_type == 'genres':
            if tag in genres:
                break
        elif model_type == 'decades':
            if tag in decades:
                break
        else:
            break
    return tag


def get_limit():
    while True:
        print("\033[1mHow many tracks would you like to model? [1-100]\033[0m")
        limit = input('> ')
        if int(limit) > 0 and int(limit) < 101:
            break
    return limit


def get_playlist(model_type, tag, limit):
    tracks = {}
    base_url = 'http://api.musicgraph.com/api/v2/playlist'
    api_url = '?api_key=' + api_key
    search_url = '&' + model_type + '=' + tag + '&limit=' + limit
    tracks_url = base_url + api_url + search_url
    tracks_request = urllib.request.urlopen(tracks_url).read().decode('utf-8')
    track_data = json.loads(tracks_request)
    for i in track_data['data']:
        title = i['title']
        artist_name = i['artist_name']
        if artist_name in tracks.keys():
            tracks[artist_name].append(title)
        else:
            tracks[artist_name] = [title]
    return tracks


def get_tracks(model_type, tag, limit):
    tracks = {}
    base_url = 'http://api.musicgraph.com/api/v2/' + model_type + '/'
    api_url = 'suggest?api_key=' + api_key
    search_url = '&prefix=' + tag + '&limit=1'
    request_url = base_url + api_url + search_url
    response = urllib.request.urlopen(request_url).read().decode('utf-8')
    response_data = json.loads(response)
    response_id = response_data['data'][0]['id']
    response_url = response_id + '/tracks?api_key=' + api_key + '&limit=' + limit
    tracks_url = base_url + response_url
    tracks_request = urllib.request.urlopen(tracks_url).read().decode('utf-8')
    tracks_data = json.loads(tracks_request)
    for i in tracks_data['data']:
        title = i['title']
        artist_name = i['artist_name']
        if artist_name in tracks.keys():
            tracks[artist_name].append(title)
        else:
            tracks[artist_name] = [title]
    return tracks


# Searching playlist by track is currently broken on MusicGraph
# def get_track_tracks(base, model, tag):
#     data = {}
#     track_request_url = base + 'suggest?api_key=' + api_key + '&prefix=' + tag + '&limit=1'
#     print(track_request_url)
#     track = urllib.request.urlopen(track_request_url).read().decode('utf-8')
#     track_data = json.loads(track)
#     track_id = track_data['data'][0]['id']
#     playlist_url = 'http://api.musicgraph.com/api/v2/playlist'
#     playlist_request_url = playlist_url + '?api_key=' + api_key + '&' + model + '=' + '95d46167-20d3-1612-7960-d54f15c7961c'
#     print(playlist_request_url)
#     print('http://api.musicgraph.com/api/v2/playlist?api_key=c8303e90962e3a5ebd5a1f260a69b138&track_ids=95d46167-20d3-1612-7960-d54f15c7961c')
#     playlist = urllib.request.urlopen(playlist_request_url).read().decode('utf-8')
#     playlist_data = json.loads(playlist)
#     print(playlist_data)
#     for i in playlist_data['data']:
#         title = i['title']
#         artist_name = i['artist_name']
#         if artist_name in data.keys():
#             data[artist_name].append(title)
#         else:
#             data[artist_name] = [title]
#     return data


def generate_lyrics(source):
    lyrics = []
    artists = []
    titles = []
    for artist in source:
        track_list = source[artist]
        for track in track_list:
            try:
                lyric = lyricwikia.get_lyrics(artist, track).rstrip()
                lyrics.append(lyric)
                titles.append(track)
                if artist not in artists:
                    artist.append(artist)
            except Exception:
                continue
    return lyrics, artists, titles


# This doesn't work
# def generate_title(titles):
#     title_list = '\n'.join(titles).rstrip()
#     print(title_list)
#     title_model = markovify.NewlineText(title_list)
#     while True:
#         markov_title = title_model.make_sentence(test_ouput=False)
#         print(markov_title)
#         if markov_title is not None:
#             break
#     print(markov_title)


# This doesn't work
# def generate_artist(artists):
#     artist_list = '\n'.join(artists).rstrip()
#     print(artist_list)
#     artist_model = markovify.NewlineText(artist_list)
#     while True:
#         markov_artist = artist_model.make_sentence(tries=100, test_ouput=False)
#         if markov_artist is not None:
#             break
#     print(markov_artist)


def generate_model(source):
    model_list = []
    for lyric in source:
        lyric_model = markovify.NewlineText(lyric)
        model_list.append(lyric_model)
    try:
        model_combo = markovify.combine(model_list)
    except ValueError as e:
        print(e)
        sys.exit()
    return model_combo


def generate_flow(model):
    lyric_list = []
    while len(lyric_list) < 4:
        sentence = model.make_sentence()
        if sentence is not None:
            lyric_list.append(sentence)
    return lyric_list


def flowriter():
    model_type = get_model_type()
    tag = get_tag(model_type)
    limit = get_limit()
    print('Getting tracks by', model_type, 'for', tag + '...')
    if model_type in ['artist', 'album']:
        source = get_tracks(model_type, tag, limit)
    elif model_type in ['genres', 'decades']:
        source = get_playlist(model_type, tag, limit)
    print("Getting lyrics for tracks...")
    lyrics, artists, titles = generate_lyrics(source)
    print("Generating models for tracks...")
    model = generate_model(lyrics)
    print("Generating markov flow...")
    flow = generate_flow(model)
    print("--------------------------------------------------------------")
    for line in flow:
        print(line)
    print("--------------------------------------------------------------")


def main():
    print(logo)
    if api_key is None:
        print("Missing API_KEY file with valid MusicGraph API key")
        sys.exit()
    while True:
        flowriter()
        while True:
            print("\033[1mWould you like to continue? [y/n]\033[0m")
            response = input('> ')
            if response in yes_words + no_words:
                break
        if response in no_words:
            break


if __name__ == '__main__':
    main()
