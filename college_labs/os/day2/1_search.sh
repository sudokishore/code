#!/bin/bash

file="file1.txt"
str="sample"

index=$(grep -bo "$str" "$file")

if [ -z "$index" ]; then
  echo "String not found in the file."
else
  index_value=$(echo "$index" | cut -d: -f1)
  echo "Index of the given string in the file: $index_value"
fi
