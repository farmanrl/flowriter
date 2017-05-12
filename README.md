# Flowriter

**By Richard Farman**

*Python API to generate lyrics by artist, album, genres, or decades*

## Description


How it works:

 * The user inputs a model type and a tag they wish to search for
 * Using the MusicGraph API, we can get a list of tracks relevant to the search parameter
 * Using the lyricwikia API, we can then fetch lyrics from those tracks
 * Using the markovify API, we can run each lyric through a markov chain generator, and combine our chains into a model
 * Using the poetrytools API, we can create lyrics that follows rhyme and rhythm

## Installation

This project requires that you install poetrytools, lyricwikia and markovify, and get an API key from MusicGraph

### poetrytools

Download [this repository](https://github.com/hyperreality/Poetry-Tools)  and use the setup.py file:

```python setup.py install```

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

This will build a model without reading or writing data.

```python3 flowriter.py data.json```

This will read and write data to and from ```data.json``` and ```data_rhyme.json```.

```python3 flowriter.py data.json edit```

This will read and write data to and from ```data.json``` and ```data_rhyme.json```.
This will edit the current model stored in ```data.json``` and ```data_rhyme.json```

### Model Type

Choose the model type that you would like to use to generate lyrics.

### Tag

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

This will determine how many tracks are retrieved for lyrics.

#### Model

The program will then get a list of tracks, fetch the lyrics for those tracks, and then generate a model.

#### Rhyme Dictionary

The program then generates a random list of sentences, and creates a dictionary using the final words of each sentence as a key, with a list of sentences corresponding to that word as a value.

#### Generating Bars

Using the model and the rhyme dictionary, we can generate a bar by creating a sentence from the model, and then finding the best rhyme from the dictionary.

We do this by evaluating both the rhyme and the rhythm of each line. Metre is evaluated using levenshtein distance to determine the most probable flow.

### Example

```
> python3 flowriter.py
===========================================================================

    ___ _                   _
   / __) |                 (_)  _
 _| |__| | ___  _ _ _  ____ _ _| |_ _____  ____
(_   __) |/ _ \| | | |/ ___) (_   _) ___ |/ ___)
  | |  | | |_| | | | | |   | | | |_| ____| |
  |_|   \_)___/ \___/|_|   |_|  \__)_____)_|


By Richard Farman
Written in Python3 with MusicGraph, lyricswikia, markovify, and poetrytools
===========================================================================
Would you like to model by artist, album, genres, or decades?
> genres
Enter the name of the genres that you would like to model:
['alternative/indie', 'blues', 'cast+recordings/cabaret', 'christian/gospel', "children's", 'classical/opera', 'comedy/spoken+word', 'country', 'electronica/dance', 'folk', 'instrumental', 'jazz', 'latin', 'new+age', 'pop', 'rap/hip+hop', 'reggae/ska', 'rock', 'seasonal', 'soul/r&b', 'soundtracks', 'vocals', 'world']
> pop
How many tracks would you like to model? [1-100]
> 20
Getting tracks by genres for pop...
Getting lyrics for tracks...
Generating models for tracks...
Generating rhyme dictionary...
Generating verses from rhyme dictionary...
---------------------------------------------------------------------------

You'll need to be that girl again
You really think I might go insane
You come and get it
I think I could be our little secret

---------------------------------------------------------------------------
Would you like to generate another verse? [y/n]
> n
Would you like to continue? [y/n]
> n
```
