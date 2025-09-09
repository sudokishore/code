#!/bin/bash

count=0
num=10

until [[ $count -eq $num ]]
do
	echo "$count"
	let count++
done
