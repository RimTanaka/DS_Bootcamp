#!/bin/sh

name_csv="../ex01/hh.csv"
if [ ! -f "$name_csv" ]; then
    echo "File hh.csv not found!"
    exit 1
fi

header=$(head -n 1 "$name_csv")

echo "$header" > hh_sorted.csv
tail -n +2 "$name_csv" | sort -t ',' -k2,2 -k1,1 >> hh_sorted.csv

echo "File hh_sorted.csv created successfully."

