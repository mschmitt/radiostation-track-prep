#!/usr/bin/env python3
import sys
import os
import requests
import slugify
import json
import datetime
from tabulate import tabulate
from operator import itemgetter
from pathlib import Path
import texttoimage
from icecream import ic
from zipfile import ZipFile
import re

# Cygwin compat fallback
if sys.version_info >= (3, 11):
    import tomllib
else:
    import tomli as tomllib

# Read config
with open(Path(__file__).with_name('jamendo.toml'), "rb") as ini:
        config = tomllib.load(ini)

album_url = sys.argv[1]
album_id = re.search(r"(\ba|album/)(\d{2,})", album_url).groups()[1]

api_base_track = 'https://api.jamendo.com/v3.0/tracks/'

query_options_track = {
        'client_id': config['jamendo_client_id'], 
        'format': 'json', 
        'album_id': int(album_id),
        'limit': 200
        }

r_tracks = requests.get(f"{api_base_track}", query_options_track)

api_base_album = 'https://api.jamendo.com/v3.0/albums/'

query_options_album = {
        'client_id': config['jamendo_client_id'], 
        'format': 'json', 
        'id': int(album_id)
        }

r_album = requests.get(f"{api_base_album}", query_options_album)

output = "\n"
output += f"Track listing for Jamendo album id {sys.argv[1]}, generated {datetime.datetime.now().replace(microsecond=0)}.\n"
output += "\n"
output += f"Title   : {r_album.json()['results'][0]['name']}\n"
output += f"Artist  : {r_album.json()['results'][0]['artist_name']}\n"
output += f"Released: {r_album.json()['results'][0]['releasedate']}\n"
output += f"URL     : {r_album.json()['results'][0]['shareurl']}\n"
output += "\n"

album_slug = slugify.slugify(f"{r_album.json()['results'][0]['artist_name']}-{r_album.json()['results'][0]['name']}-jamendo-{r_album.json()['results'][0]['id']}", lowercase=False)


r_zip = requests.get(r_album.json()['results'][0]['zip'])
with open('jamendo_tmp.zip', 'wb') as tmpzip:
    tmpzip.write(r_zip.content)

with ZipFile('jamendo_tmp.zip') as z:
    z.extractall(album_slug)
os.unlink('jamendo_tmp.zip')

with open(f"{album_slug}/url.txt", 'w') as urltxt:
    urltxt.write(r_album.json()['results'][0]['shareurl'])

table = list()
for track in (r_tracks.json())['results']:
        table.append([track['position'], track['name'], track['artist_name'], track['license_ccurl']])

output += tabulate(sorted(table, key=itemgetter(0)), headers=['#', 'Track', 'Artist', 'License URL'])
output += "\n"
texttoimage.convert(output, font_name=f"{Path(__file__).resolve().parent}/LiberationMono-Regular.ttf", image_file=f"{album_slug}/proof.png", color="white")
print(output)

