#!/usr/bin/bash

function real-estate {
    city=$1
    zipcode=$2

    echo "City = $city, Zipcode = $zipcode"

    # Simple script to get all the real estate data for a given city
    directory="$city/real-estate"

    if [ ! -d "$directory" ]; then
        mkdir -p "$directory"
    fi

    # curl -L http://www.quandl.com/api/v3/datasets/ZILL/Z"$zipcode"_A.csv -o $city/real-estate/$zipcode-raw.csv
    curl -sL http://www.quandl.com/api/v3/datasets/ZILL/Z"$zipcode"_"A.csv?api_key=yo1tszfwCLdpSbc6gqJn" | sed -En -e 's/^([0-9]{4})-[0-9]{2}-[0-9]{2},(.*$)/\1,\2/p' | awk -F, '{a[$1]+=$2; b[$1]+=1} END { for (i in a) {printf "%d,%f\n", i, a[i]/b[i]}}' | sort > "$directory/$zipcode.csv"
}

