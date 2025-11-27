#!/bin/sh

input_file="../ex03/hh_positions.csv"
output_file="hh_uniq_positions.csv"

if [ ! -f "$input_file" ]; then
    echo "File $input_file not found!"
    exit 1
fi

{
    echo '"name","count"'
    tail -n +2 "$input_file" | cut -d',' -f3 | sort | uniq -c | sort -nr | awk '{print "" $2 "," $1 ""}'
} > "$output_file"

echo "File $output_file created successfully."

