#!/bin/bash

# And operator
read -p "Enter your age : " age 
read -p "Enter your country : " country

# -eq compares two numbers but not strings
if [[ $age -ge 18 ]] && [[ $country ==  "India" ]]
then
	echo "You can vote."
else
	echo "You can't vote"
fi
