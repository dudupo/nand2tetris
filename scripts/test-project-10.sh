#!/bin/bash

for i in ./projects/10/*
do
  if [ "$i" != "./projects/10/compiler" ]; then
    #statements
    echo -e "\ncompiling project $i :"
    for j in $i/*.jack
    do
      echo -e "\t${j%.*}_out.xml"
      python ./projects/10/compiler/main.py $j
      ./tools/TextComparer.bat "${j%.*}_out.xml"  "${j%.*}.xml"
    done
  fi
done
