#!/bin/sh

curl "https://api.hh.ru/vacancies?text=data%20scientist&per_page=20" \
     | jq '.' > "hh.json"
