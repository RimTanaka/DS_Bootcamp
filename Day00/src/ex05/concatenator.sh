#!/bin/sh

output_file="hh_combined.csv"
csv_files=$(ls *.csv | grep -v "^$output_file")

if [ -z "$csv_files" ]; then
  echo "No files to concatenate!"
  exit 1
fi

head -n 1 $(echo "$csv_files" | head -n 1) > "$output_file"

for file in $csv_files; do
  tail -n +2 "$file" >> "$output_file"

  rm "$file"
  echo "Deleted file: $file"
done

echo "Concatenation completed. Result stored in $output_file."
