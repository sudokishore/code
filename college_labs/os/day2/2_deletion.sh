#!/bin/bash

file="file2.txt"

i=1

while read line; do
  if [ $(($i % 2)) -eq 1 ]; then
    echo "$line" >>"$file.tmp"
  fi
  let i=i+1
done <"$file"

mv "$file.tmp" "$file"
echo "After removing, new file content is: "
cat -n "$file"
