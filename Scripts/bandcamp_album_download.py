#!/usr/bin/env python3
import yt_dlp
import eyed3
import pathlib
import os
import sys
import asyncio
import pyppeteer
from slugify import slugify
from icecream import ic
from urllib.parse import urlparse

url = sys.argv[1]
up = urlparse(url)
slug = slugify(f"{up.netloc}{up.path}")

pathlib.Path.mkdir(slug)
os.chdir(slug)

def hook(data):
    if data['status'] != 'finished': return
    af = eyed3.load(data['filename'])
    af.initTag()
    af.tag.artist    = data['info_dict']['artist']
    af.tag.title     = data['info_dict']['track']
    af.tag.album     = data['info_dict']['album']
    af.tag.track_num = data['info_dict']['track_number']
    af.tag.save()

with yt_dlp.YoutubeDL({'progress_hooks': [hook]}) as ydl:
    ydl.download(url)

with open('url.txt', 'w') as url_fh:
    url_fh.write(f"{url}\n")

async def screenshot():
    browser = await pyppeteer.launch({'executablePath': 'chromium'})
    page = await browser.newPage()
    page.setDefaultNavigationTimeout(100000)
    await page.goto(url, { 'waitUntil': 'networkidle2' })
    await page.evaluate(f"""() => {{
        document.getElementsByTagName('page-footer')[0].style.display = 'none';
        document.getElementsByClassName('tos-update')[0].style.display = 'none';
    }}""")
    await page.screenshot({'path': 'proof.png', 'fullPage': True})
    await page.close()
    await browser.close()
asyncio.get_event_loop().run_until_complete(screenshot())
