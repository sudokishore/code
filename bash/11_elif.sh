#!/bin/bash

read -p "Enter your marks : " marks

if [[ $marks -ge 90 ]]
then
	echo "First Division"
elif [[ $marks -ge 80 && $marks -lt 90 ]]
then
	echo "Second Division"
else
	echo "Less than 80"
fi
