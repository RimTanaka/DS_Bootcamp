#!/bin/sh

name_csv="../ex02/hh_sorted.csv"

if [ ! -f "$name_csv" ]; then
    echo "File hh_sorted.csv not found!"
    exit 1
fi

header=$(head -n 1 "$name_csv")

tail -n +2 "$name_csv" | while IFS=, read -r id created_at name has_test alternate_url; do
    position=""
    if echo "$name" | grep -q -i "Junior"; then
        position="Junior"
    fi
    if echo "$name" | grep -q -i "Middle"; then
        if [ -n "$position" ]; then
            position="$position/Middle"
        else
            position="Middle"
        fi
    fi
    if echo "$name" | grep -q -i "Senior"; then
        if [ -n "$position" ]; then
            position="$position/Senior"
        else
            position="Senior"
        fi
    fi

    if [ -z "$position" ]; then
        position="-"
    fi

    echo "\"$id\",\"$created_at\",\"$position\",$has_test,\"$alternate_url\"" >> hh_positions.csv
done

sed -i "1i$header" hh_positions.csv

echo "File hh_positions.csv created successfully."

