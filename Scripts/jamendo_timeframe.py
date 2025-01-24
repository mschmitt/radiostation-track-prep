#!/usr/bin/env python3
import sys
import math
from pathlib import Path
import requests
from tabulate import tabulate
from icecream import ic
import argparse

# Cygwin compat fallback
if sys.version_info >= (3, 11):
    import tomllib
else:
    import tomli as tomllib

# Read config
with open(Path(__file__).with_name('jamendo.toml'), "rb") as ini:
    config = tomllib.load(ini)

parser = argparse.ArgumentParser(description='Generate Jamendo listing for timeframe.')
parser.add_argument('-f', '--from-date', help='start date YYYY-MM-DD', required=True)
parser.add_argument('-t', '--to-date', help='end date YYYY-MM-DD', required=True)
args = parser.parse_args()

api_base = 'https://api.jamendo.com/v3.0'

query_options={
        'client_id': config['jamendo_client_id'],
        'format': 'json',
        'order': 'releasedate',
        'limit': 200,
        'datebetween': f"{args.from_date}_{args.to_date}",
        'ccsa': False,
        'ccnd': False,
        'ccnc': False
        }

request_count = 1
try:
    r_tracks=requests.get(f"{api_base}/tracks", query_options | {'tags': 'electronic', 'type': 'single albumtrack'})
    tracks=r_tracks.json()['results']
except Exception as e:
    ic(e)
    sys.exit(255)

# At this point, I have all relevant individual tracks from the timeframe. Start building my inventory.
raw_order = list()
album_ids = set()
for track in tracks:
    if track['album_id'] == '':
        # This is a single.
        track.pop('waveform', None)
        track['AA_order_type'] = 'single'
        raw_order.append(track)
    elif track['album_id'] not in album_ids:
        # This is a track from an album that features at least one relevant song.
        album_ids.add(track['album_id'])
        # Retrieve details for this album.
        try:
            request_count += 1
            r_album = requests.get(f"{api_base}/albums", query_options | {'id': track['album_id']})
            album = r_album.json()['results'][0]
        except Exception as e:
            ic(e)
            sys.exit(255)
        album['AA_order_type'] = 'album'
        raw_order.append(album)
        ## Retrieve list of all songs from this album.
        ## First a raw list of ids
        #try:
        #    request_count += 1
        #    r_albumtracks = requests.get(f"{api_base}/albums/tracks", query_options | {'id': track['album_id']})
        #    albumtracks = r_albumtracks.json()['results'][0]['tracks']
        #except Exception as e:
        #    ic(e)
        #    sys.exit(255)
        ## Next, song details for each id
        #album_track_id_list = list()
        #for albumtrack in albumtracks:
        #    album_track_id_list.append(albumtrack['id'])
        #try:
        #    request_count += 1
        #    r_this_album_tracks = requests.get(f"{api_base}/tracks", query_options | {'id': ' '.join(album_track_id_list)})
        #    this_album_tracks = r_this_album_tracks.json()['results']
        #except Exception as e:
        #    ic(e)
        #    sys.exit(255)
        #for this_album_track in this_album_tracks:
        #    this_album_track.pop('waveform', None)
        #    this_album_track['AA_order_type'] = 'track'
        #    raw_order.append(this_album_track)
        #print(f"entries={len(raw_order)}, requests={request_count}")
        #time.sleep(1)

def mmss (secs):
    return f"{math.floor(secs / 60)}:{secs % 60:02}"

table = list()
for entry in raw_order:
    hyperlink = f"<a href='{entry['shareurl']}' target='_blank'>{entry['name']}</a>"
    if entry['AA_order_type'] == 'single':
        table.append(['Single', entry['releasedate'], entry['artist_name'], hyperlink, mmss(entry['duration'])])
    if entry['AA_order_type'] == 'album':
        table.append(['Album', entry['releasedate'], entry['artist_name'], hyperlink, ''])
print("<html><body>")
print(tabulate(table, tablefmt="unsafehtml", headers=["Type","Release", "Artist", "Title", "Duration"]))
print("</body></html>")
