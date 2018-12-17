import requests
from bs4 import BeautifulSoup
import nltk

base_url = "https://api.genius.com"
headers = {'Authorization': 'Bearer 90fDPe_mgCL9gXyA9bZBge-mXZHZO4p-tyge9rByM0iSJDTULzVLYQpwawHnHecf'}


def lyrics_from_song_api_path(song_title,artist_name):
  search_url = base_url + "/search"
  data = {'q': song_title}
  response = requests.get(search_url, data=data, headers=headers)
  json = response.json()
  song_info = None
  for hit in json["response"]["hits"]:
    if hit["result"]["primary_artist"]["name"].lower() == artist_name.lower() or hit["result"]["primary_artist"]["name"].lower() in artist_name.lower() or artist_name.lower() in hit["result"]["primary_artist"]["name"].lower():
      song_info = hit
      break
  if song_info:
    song_api_path = song_info["result"]["api_path"]
    song_url = base_url + song_api_path
    response = requests.get(song_url, headers=headers)
    json = response.json()
    path = json["response"]["song"]["path"]
    #gotta go regular html scraping... come on Genius
    page_url = "http://genius.com" + path
    page = requests.get(page_url)
    html = BeautifulSoup(page.text, "html.parser")
    #remove script tags that they put in the middle of the lyrics
    [h.extract() for h in html('script')]
    #at least Genius is nice and has a tag called 'lyrics'!
    lyrics = html.find("div", class_="lyrics").get_text() #updated css where the lyrics are based in HTML
    return lyrics
  else:
    return ""



#example use below:

kendrick="""Fuck Your Ethnicity
Hol' Up
A.D.H.D
No Make-Up (Her Vice)
Tammy's Song (Her Evils)
Chapter Six
Ronald Reagan Era (His Evils)
Poe Mans Dreams (His Vice)
The Spiteful Chant
Chapter Ten
Keisha's Song (Her Pain)
Rigamortus
Kush & Corinthians (His Pain)
Blow My High (Members Only)
Ab-Soul's Outro
HiiiPoWeR
Sherane A.K.A Master Splinter's Daughter
Bitch, Don't Kill My Vibe
Backseat Freestyle
The Art Of Peer Pressure
Money Trees
Poetic Justice
Good Kid
m.A.A.d City
Swimming Pools (Drank)
Sing About Me, I'm Dying Of Thirst
Real
Compton
The Recipe
Wesley's Theory
For Free? (Interlude)
King Kunta
Institutionalized
These Walls
u
Alright
For Sale? (Interlude)
Momma
Hood Politics
How Much A Dollar Cost
Complexion (A Zulu Love)
The Blacker The Berry
You Ain't Gotta Lie (Momma Said)
i
Mortal Man
BLOOD.
DNA.
YAH.
ELEMENT.
FEEL.
LOYALTY.
PRIDE.
HUMBLE.
LUST.
LOVE.
XXX.
FEAR.
GOD.
DUCKWORTH."""


from corpus import x

lyrics=''

for artist in x.keys():
    for song in x[artist].split('\n'):
        lyrics+= lyrics_from_song_api_path(song,artist)

with open("lyrics.txt", "w", encoding="utf-8") as f:
    f.write(lyrics)