#!/bin/bash

echo $PWD
cd Charts_2
for f in *.PDF; do
  convert ./"$f[0]" ./"${f%.PDF}.png"
  echo "${f} converted"
done
