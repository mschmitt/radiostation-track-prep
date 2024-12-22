#!/usr/bin/env python3
import sys
import requests
import json
from tabulate import tabulate
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

api_base = 'https://api.jamendo.com/v3.0/tracks/'

query_options={
        'client_id': config['jamendo_client_id'], 
        'format': 'json', 
        'order': 'releasedate',
        'limit': 200,
        'tags': 'electronic',
        'datebetween': '2010-01-01_2010-12-31',
        'ccsa': False,
        'ccnd': False,
        'ccnc': False
        }

r_tracks=requests.get(f"{api_base}", query_options)

table = list()
for track in reversed((r_tracks.json())['results']):
    table.append([track['releasedate'], track['name'][:30], track['artist_name'][:30], f"https://jamen.do/l/{track['album_id']}", f"https://jamen.do/t/{track['id']}"])

print(tabulate(table))
