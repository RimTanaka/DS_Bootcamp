#!/bin/sh

if [ ! -f "../ex00/hh.json" ]; then
    echo "File hh.json not found!"
    exit 1
fi

echo "id,created_at,name,has_test,alternate_url" > hh.csv
jq -r -f filter.jq ../ex00/hh.json | jq -r '. | "\(.id),\(.created_at),\(.name),\(.has_test),\(.alternate_url)"' >> hh.csv

if [ $? -eq 0 ]; then
    echo "CSV file created successfully: hh.csv"
else
    echo "Failed to create CSV file"
    exit 1
fi

