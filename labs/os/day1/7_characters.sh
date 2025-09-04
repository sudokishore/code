#!/bin/bash

file="/home/kishore/code/labs/os/file2.txt"

characters=$(wc -m <"$file")
words=$(wc -w <"$file")
lines=$(wc -l <"$file")

cat "$file"

echo "No of characters in this file : $characters"
echo "No of words in this file : $words"
echo "No of lines in this file : $lines"
