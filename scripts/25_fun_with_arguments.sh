#!/bin/bash

sum() {
	local num1=$1
	local num2=$2
	let num3=$num1+$num2
	echo "Sum of $num1 and $num2 is $num3."
}

sum 10 25
