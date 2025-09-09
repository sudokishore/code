#!/bin/bash

d1="dir1"
d2="dir2"

files1=$(ls "$d1")
files2=$(ls "$d2")

while read f1; do
  while read f2; do
    if [ "$f1" == "$f2" ]; then
      echo "Found duplicate: $d1/$f1 and $d2/$f2. Removed $d1/$f1"
      rm "$d1/$f1"
    fi
  done <<<"$files2"
done <<<"$files1"

echo "All duplicate files have been removed."
