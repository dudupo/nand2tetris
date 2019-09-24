#!/bin/bash

# for i in ./projects/10/*
# do
#   if [ "$i" != "./projects/10/compiler" ]; then
#     #statements
#     echo -e "\ncompiling project $i :"
#     for j in $i/*.jack
#     do
#       echo -e "\t${j%.*}_out.xml"
#       python ./projects/10/compiler/main.py $j
#       ./tools/TextComparer.bat "${j%.*}_out.xml"  "${j%.*}.xml"
#     done
#   fi
# done

for i in ./projects/12/*.jack
do
  if [[ -f $i  ]]; then
    ./tools/JackCompiler.bat $i
    for j in ./projects/12/*
    do
      if [[ -d $j  ]]; then
        cp ${i%.*}.vm $j/
      fi
    done
  fi
done

for j in ./projects/12/*
do
  if [[ -d $j  ]]; then
    ./tools/JackCompiler.bat "$j/Main.jack"
  fi
done

for j in ./projects/12/*/*.tst
do
  echo "testing : $j"
  ./tools/VmEmulator.bat  "$j"
done

# ./tools/JackCompiler.bat ./projects/12/Math.jack
# ./tools/JackCompiler.bat ./projects/12/Sys.jack
# cp ./projects/12/Math.vm  ./projects/12/MathTest/
# cp ./projects/12/Sys.vm  ./projects/12/MathTest/
# ./tools/JackCompiler.bat ./projects/12/MathTest/Main.jack
# ./tools/VmEmulator.bat  ./projects/12/MathTest/MathTest.tst
