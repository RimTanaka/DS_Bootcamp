#!/bin/sh

input_file="../ex03/hh_positions.csv"

if [ ! -f "$input_file" ]; then
  echo "Input file not found!"
  exit 1
fi

header=$(head -n 1 "$input_file")

tail -n +2 "$input_file" | cut -d',' -f2 | cut -d'T' -f1 | tr -d '"'| sort | uniq | while read date; do
  output_file="$date.csv"

  echo "$header" > "$output_file"
  grep "$date" "$input_file" >> "$output_file"
  echo "Created $output_file"
done

echo "Partitioning completed."
