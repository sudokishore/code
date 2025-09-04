#!/bin/bash

while read myVar
do
	echo "Value from file is : $myVar"
done < names.txt
