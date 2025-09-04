#!/bin/bash

# My array
arr=(1 2 "Kishore" 5.9 Nayak)

echo "${arr[0]}"

# To print the entire array :
echo "All values in array : ${arr[*]}"

# To print the length of the array :
echo "Array length : ${#arr[*]}"

# Array Slicing
echo "Values starting from index 3 are : ${arr[*]:3}"
echo "Values from index 1 to 3 are : ${arr[*]:1:3}"
echo "Values upto index 3 are : ${arr[*]::3}"

# Adding elements to an array
arr+=(New 69)
echo "Values of new array : ${arr[*]}"
echo "Length of new array : ${#arr[*]}"
