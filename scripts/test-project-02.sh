#!/bin/bash

for i in ../projects/02/*.tst
do
  echo $i
  ../tools/HardwareSimulator.bat $i
done
