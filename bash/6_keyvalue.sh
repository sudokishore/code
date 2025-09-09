#!/bin/bash

# Key Value is nothing but a hashmap or a dictionary
declare -A myarr
myarr=([name]=Kishore [age]=21)

echo "My name is ${myarr[name]} & my age is ${myarr[age]}"
