#!/bin/bash

for i in ../projects/01/*.tst
do
  echo $i
  ../tools/HardwareSimulator.bat $i
done
