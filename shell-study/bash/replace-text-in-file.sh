#!/bin/bash

# 결과 파일을 저장할 out 디렉터리가 없으면 생성
mkdir -p ../out

sed 's/${env}/goenv/g' ./data/input.txt > ../out/output.txt
sed -i '' 's/${service}/goservice/g' ../out/output.txt

cat ../out/output.txt