#!/bin/bash

# hello="HELLO"
# hello=$(echo "$hello" | tr '[:upper:]' '[:lower:]')
# hello="$hello world!"
# echo $hello

# if [ "$hello" == "hello world" ]; then
# 	echo "no"
# 	exit
# fi

# echo "end"

echo -n "Would you like to distribute the image to the XXXXX production service(Y/N)"
read YN

YN=$(echo "$YN" | tr '[:upper:]' '[:lower:]')
YN=${YN:0:1}
echo $YN

if [ "${YN:0:1}" != "y" ]; then
	echo "Build Image Stopped"
	exit
if