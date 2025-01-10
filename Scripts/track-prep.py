#!/usr/bin/env python3
import sys
import argparse
import eyed3
from slugify import slugify
from pathlib import Path
from icecream import ic

parser = argparse.ArgumentParser(description='Prepare tracks for playing')
parser.add_argument('-n', '--note', help='local usage note', required=True)
parser.add_argument('-l', '--license', help='local license tag', required=True)
parser.add_argument('-u', '--url', help='url-file (txt next to target file)', required=True)
parser.add_argument('-p', '--proof', help='proof (png next to target file)', required=True)
parser.add_argument('-d', '--done', help='list of treated files (txt next to target file)', required=True)
parser.add_argument('files', help='any number of files', nargs='+')
args = parser.parse_args()

for file in args.files:
    file_slug = slugify(Path(file).name)
    proof = Path(file).parent / args.proof
    url_file = Path(file).parent / args.url
    done_file = Path(file).parent / args.done
    try:
        with open(url_file, 'r') as u:
            url = u.readline().strip()
    except Exception as e:
        print(f"{url_file}: {e}")
    try:
        with open(done_file, 'r') as d:
            if file_slug in d.read():
                #print(f"Already tagged: {file}")
                continue
    except:
        pass
    try:
        af = eyed3.load(file)
        af.tag.user_text_frames.set(args.note, "Local usage note")
        af.tag.user_text_frames.set(args.license, "Local license tag")
        af.tag.user_text_frames.set(url,"Local download URL")
        with open(proof, 'rb') as p:
            img = p.read()
            af.tag.images.set(eyed3.id3.frames.ImageFrame.OTHER, img, "image/png", u"Proof of license at download")
        af.tag.save()
    except Exception as e:
        print(f"{file}: {e}")
    try:
        with open(done_file, "a") as d:
            d.write(f"{file_slug}\n")
            print(f"Tagged: {file}")
    except Exception as e:
        print(f"Error tagging file {file}: {e}")
