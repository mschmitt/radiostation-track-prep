all:
	find Music/PD/ -type f -print0 | xargs -0 Scripts/embed-proof-pd.sh
	find Music/BY/ -type f -print0 | xargs -0 Scripts/embed-proof-by.sh
	systemctl start --user nextcloudcmd.service
