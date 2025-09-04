#!/bin/bash

read -p "Enter your marks : " marks

if [[ $marks -gt 33 ]]
then
	echo "Passed"
else
	echo "Failed"
fi
