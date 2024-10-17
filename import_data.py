import os
import time
import requests
import subprocess
import json

def wait_for_mongodb():
    while True:
        try:
            subprocess.run(["mongosh", os.environ['MONGO_URI'], "--eval", "db.adminCommand('ping')"], 
                           check=True, capture_output=True)
            print("MongoDB is available. Proceeding with data import.")
            return
        except subprocess.CalledProcessError:
            print("MongoDB is not available yet. Waiting...")
            time.sleep(1)

def download_and_import(url, collection_name):
    response = requests.get(url)
    filename = f"{collection_name}.json"
    
    with open(filename, 'w') as f:
        json.dump(response.json(), f)
    
    mongo_uri = os.environ['MONGO_URI']
    db_name = 'sample_data'
    
    command = [
        "mongoimport",
        "--uri", mongo_uri,
        "--db", db_name,
        "--collection", collection_name,
        "--file", filename,
        "--jsonArray"
    ]
    
    subprocess.run(command, check=True)
    
    # Get count of imported documents
    count_command = [
        "mongosh", 
        mongo_uri,
        "--eval", 
        f"db.getSiblingDB('{db_name}').{collection_name}.count()"
    ]
    result = subprocess.run(count_command, capture_output=True, text=True, check=True)
    count = result.stdout.strip().split('\n')[-1]
    
    print(f"Imported {count} documents into {collection_name}")

def main():
    wait_for_mongodb()
    
    download_and_import(os.environ['CITY_INSPECTIONS_URL'], 'city_inspections')
    download_and_import(os.environ['COMPANIES_URL'], 'companies')

if __name__ == "__main__":
    main()
