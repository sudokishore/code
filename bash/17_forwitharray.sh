#!/bin/bash

arr=( 1 2 3 Hello Hi )

len=${#arr[*]}

	for(( i=0; i<$len; i++ ))
do
	echo "Element is : ${arr[i]}"
done
