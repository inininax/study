#!/bin/bash

sed 's/${env}/goenv/g' ./data/input.txt > ../out/output.txt
sed -i '' 's/${service}/goservice/g' ../out/output.txt

cat ../out/output.txt