# Flowriter

**By Richard Farman**

*Python API to generate lyrics by artist, album, genres, or decades*

## Description


How it works:

 * The user inputs a model type and a tag they wish to search for
 * Using the MusicGraph API, we can get a list of tracks relevant to the search parameter
 * Using the lyricwikia API, we can then fetch lyrics from those tracks
 * Using the markovify API, we can run each lyric through a markov chain generator, and combine our chains into a model
 * We can then randomly generate sentences based on that model

## Installation

This project requires that you install lyricwikia and markovify, and get an API key from MusicGraph

### lyricwikia

The package [lyricwikia](https://pypi.python.org/pypi/lyricwikia) is on PyPI, so you can install it using pip:

```pip install lyricwikia```

Otherwise download [this repository](https://github.com/enricobacis/lyricwikia)  and use the setup.py file:

```python setup.py install```

### markovify

The package [markovify](https://pypi.python.org/pypi/markovify) is also on PyPI, so you can install it using pip:

```pip install markovify```

Otherwise download [this repository](https://pypi.python.org/pypi/markovify)  and use the setup.py file:

```python setup.py install```

### MusicGraph

To get an API key for [MusicGraph](https://developer.musicgraph.com/), sign up on their website and generate a new key through their admin/applications menu.


## Usage

Start by running the program through the command line.

```python3 flowriter.py```

The program will then require some user input.

```Would you like to model by artist, album, genres, or decades?```

Choose the model type that you would like to use to generate lyrics.

### Tag

```Enter the name of the tag that you would like to model:```

Artists and albums will be searched for most relevant result, genres and decades should be one of the following:

Genres:

* Alternative/Indie
* Blues
* Cast Recordings/Cabaret
* Christian/Gospel
* Children's
* Classical/Opera
* Comedy/Spoken Word
* Country
* Electronica/Dance
* Folk
* Instrumental
* Jazz
* Latin
* New Age
* Pop
* Rap/Hip Hop
* Reggae/Ska
* Rock
* Seasonal
* Soul/R&B
* Soundtracks
* Vocals
* World

Decades:

* 1890s
* 1900s
* 1910s
* 1920s
* 1930s
* 1940s
* 1950s
* 1960s
* 1970s
* 1980s
* 1990s
* 2000s
* 2010s

#### Limit

```How many tracks would you like to model? [1-100]```

This will determine how many tracks are retrieved for lyrics.

#### Model

The program will then get a list of tracks, fetch the lyrics for those tracks, and then generate a model.

```
Getting tracks by model for tag...
Getting lyrics for tracks...
Generating models for tracks...
Generating markov flow...
```

At last, the program will print four random sentences from the model.

```Would you like to continue? [y/n]```

You can choose to continue, or exit the program.

### Example
```
==============================================================
    ___ _                   _
   / __) |                 (_)  _
 _| |__| | ___  _ _ _  ____ _ _| |_ _____  ____
(_   __) |/ _ \| | | |/ ___) (_   _) ___ |/ ___)
  | |  | | |_| | | | | |   | | | |_| ____| |
  |_|   \_)___/ \___/|_|   |_|  \__)_____)_|

By Richard Farman
Written in Python3 with MusicGraph, lyricswikia, and markovify
==============================================================
Would you like to model by artist, album, genres, or decades?
> genres
Enter the name of the genres that you would like to model:
> pop
How many tracks would you like to model? [1-100]
> 40
Getting tracks by genres for pop...
Getting lyrics for tracks...
Generating models for tracks...
Generating markov flow...
--------------------------------------------------------------
You are inclined to make it change
And I won’t judge you
Oh, if you knock it, ain't no other way
I tell her baby, baby, baby, baby, baby, baby
--------------------------------------------------------------
Would you like to continue? [y/n]
> n
```
