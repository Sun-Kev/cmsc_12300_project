#!/bin/bash
# from http://www.compciv.org/topics/bash/loops/
echo '' > download_links.txt
for line in $(cat aleppoids.txt)
do
	echo $line
	planet data download --activate-only --item-type PSScene3Band --asset-type analytic --string-in id $line  --quiet | jq '.location' >> download_links.txt

done
