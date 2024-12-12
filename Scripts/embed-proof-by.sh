#!/usr/bin/env bash
set -o errexit

me_path="$(readlink -f "$0")"
me_dir="$(dirname "${me_path}")"
me_base="$(basename "${me_path}")"

function errorexit() {
	trap - ERR
	printf "Error on line %s\n" "$(caller)"
	exit 1
}
trap errorexit ERR

declare -a noproof
for file in "$@"
do
	if [[ "${file}" =~ mp3$ ]] 
	then
		if [[ -e "$(dirname "${file}")/proof.png" ]]
		then
			true # Used to have debug output here
		else
			noproof+=("${file}")
			continue
		fi
	else
		continue
	fi
	if [[ "$(getfattr --only-values -n user.license_tagged "${file}")" == 'true' ]]
	then
		printf "Already tagged: %s\n" "${file}"
		continue
	fi
	url="$(head -n 1 "$(dirname "${file}")/url.txt")
	printf "Tagging: %s\n" "${file}"
	eyeD3 -2 --user-text-frame "Local usage note":"This file was downloaded under a Creative Commons CC-BY license and is being used accordingly. Screenshot archived and embedded as proof." "${file}"
	eyeD3 -2 --add-image "$(dirname "${file}")/proof.png:OTHER:Proof of license at download" "${file}"
	eyeD3 -2 --user-text-frame "Local license tag":"CC-BY" "${file}"
	eyeD3 -2 --user-text-frame "Local download URL":"${url}" "${file}"
	setfattr --name user.license_tagged --value true "${file}"
done

for i in "${noproof[@]}"
do 
	printf "No proof for: %s\n" "${i}"
done


