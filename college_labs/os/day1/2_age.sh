#!/bin/bash

read -p "Enter your age : " age

if [[ $age -ge 18 ]]
then
	echo "You are adult."
else 
	echo "You are minor."
fi
