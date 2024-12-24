all:
	find Music/BY/ -type f -iname '*mp3' -print0 | xargs --no-run-if-empty -0 Scripts/track-prep.py -n 'This file was downloaded under a Creative Commons CC-BY license and is being used accordingly. Screenshot archived and embedded as proof.' -l 'CC-BY' -u url.txt -p proof.png -d tagged.txt
	find Music/PD/ -type f -iname '*mp3' -print0 | xargs --no-run-if-empty -0 Scripts/track-prep.py -n 'This file was downloaded under a Creative Commons CC0 or Public Domain license and is being used accordingly. Screenshot archived and embedded as proof.' -l 'CC0/PD' -u url.txt -p proof.png -d tagged.txt
