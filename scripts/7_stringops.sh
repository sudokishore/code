#!/bin/bash

str="Hey Buddy, How are you?"

strlen=${#str}
echo "String length is : $strlen" 


echo "Upper Case : ${str^^}"
echo "Lower Case : ${str,,}"

# Replace one word with another
str2=${str/Buddy/Nishant}
echo "New string is : ${str2}"

# To slice a string
str3=${str:4:5} # Start from index 4 take 5 characters
echo "After slicing : ${str3}"
