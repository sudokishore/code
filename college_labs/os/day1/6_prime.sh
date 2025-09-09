#!/bin/bash

read -p "Enter a positive number : " num

for (( i=1; i<=$num; i++ ))
do
	if [[ $i -eq 1 ]]
	then
		echo "1 is neither prime nor composite."
		continue
	fi

	if [[ $i -eq 2 ]]
	then
		echo "2 is a prime number."
		continue
	fi


	count=0
	for (( j=2; j<$i; j++ ))
	do
		let temp=$i%$j	
		if [[ $temp -eq 0 ]]
		then
			let count++
			break
		fi
	done
	if [[ $count == 0 ]]
	then
		echo "$i is a prime number."
	fi
done
