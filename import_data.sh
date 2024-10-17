#!/bin/bash

wait_for_mongodb() {
    while ! mongosh "$MONGO_URI" --eval "db.adminCommand('ping')" &>/dev/null; do
        echo "MongoDB is not available yet. Waiting..."
        sleep 1
    done
    echo "MongoDB is available. Proceeding with data import."
}

download_and_import() {
    url="$1"
    collection_name="$2"
    filename="${collection_name}.json"

    echo "Downloading $collection_name dataset..."
    wget -O "$filename" "$url"

    echo "Importing $collection_name into MongoDB..."
    mongoimport --uri "$MONGO_URI" \
                --db admin \
                --collection "$collection_name" \
                --file "$filename" \
                --jsonArray

    count=$(mongosh "$MONGO_URI" --quiet --eval "db.getSiblingDB('sample_data').$collection_name.count()")
    echo "Imported $count documents into $collection_name"
}

main() {
    wait_for_mongodb

    download_and_import "$CITY_INSPECTIONS_URL" "city_inspections"
    download_and_import "$COMPANIES_URL" "companies"
}

main
