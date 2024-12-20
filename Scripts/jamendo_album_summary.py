#!/usr/bin/env python3
import sys
import requests
import json
import datetime
from tabulate import tabulate
from operator import itemgetter
from pathlib import Path
from icecream import ic

# Cygwin compat fallback
if sys.version_info >= (3, 11):
    import tomllib
else:
    import tomli as tomllib

# Read config
with open(Path(__file__).with_name('jamendo.toml'), "rb") as ini:
        config = tomllib.load(ini)

api_base_track = 'https://api.jamendo.com/v3.0/tracks/'

query_options_track = {
        'client_id': config['jamendo_client_id'], 
        'format': 'json', 
        'album_id': sys.argv[1],
        'limit': 200
        }

r_tracks=requests.get(f"{api_base_track}", query_options_track)

api_base_album = 'https://api.jamendo.com/v3.0/albums/'

query_options_album = {
        'client_id': config['jamendo_client_id'], 
        'format': 'json', 
        'id': sys.argv[1]
        }

r_album=requests.get(f"{api_base_album}", query_options_album)

print()
print(f"Track listing for Jamendo album id {sys.argv[1]}, generated {datetime.datetime.now().replace(microsecond=0)}.")
print()
print(f"Title   : {r_album.json()['results'][0]['name']}")
print(f"Artist  : {r_album.json()['results'][0]['artist_name']}")
print(f"Released: {r_album.json()['results'][0]['releasedate']}")
print(f"URL     : {r_album.json()['results'][0]['shareurl']}")
print()

table = list()
for track in (r_tracks.json())['results']:
        table.append([track['position'], track['name'], track['artist_name'], track['license_ccurl']])

print(tabulate(sorted(table, key=itemgetter(0)), headers=['#', 'Track', 'Artist', 'License URL']))
print()
