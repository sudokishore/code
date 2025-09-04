#!/bin/bash

# Getting values from a file names.txt
FILE="/home/kishore/Code/Scripts/names.txt"

for name in $(cat $FILE)
do
	echo "$name"
done
