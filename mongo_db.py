from flask import Flask
import pymongo

# Connection string from MongoDb Atlas
CONN_STRING = "mongodb+srv://shanu05official:fhcnVcJjMvnefACu@cluster0.otbkjtz.mongodb.net/?retryWrites=true&w=majority"

# Initiating mongodb client
def open_mongo_diseases(index):
    client = pymongo.MongoClient(CONN_STRING)
    # Loading database
    db = client.get_database('cropguard')
    collection = db['cropguard-collection']
    print("collection - ", collection)
    print("index- ", index)

    # Disease data dictionary is sourced from the collection
    disease_data = collection.find_one({'Id': int(index)})

    # CLI: Printing the dictionary
    print(disease_data)
    print(type(disease_data))

    # Closing the MongoDB session after sourcing data.
    client.close()
    return disease_data

def new_data(entry_name, caused_by, about, Id, cure):
    # Adding the data in MongoDB
    # Opening connection
    client = pymongo.MongoClient(CONN_STRING)
    # Loading database
    db = client.get_database('cropguard')
    collection = db['cropguard-collection']

    # Creating dictionary
    entry_dict = {
        "name": entry_name,
        "caused_by": caused_by,
        "about": about,
        "Id": Id,
        "cure": cure
    }

    # Checking for duplicacy
    dupl_data = collection.find()

    # Variable to check if duplicate is present
    counter=0

    # Checking for redundancy
    for entry in dupl_data:
        if entry['name'] == entry_name:
            print("Crop already entered by user.")
            alert = "Crop already entered by user."
            counter = 1
            break
    
    if counter == 0:
        # Inserting the dictionary
        collection.insert_one(entry_dict)

        print("Entry Successful")
        alert = "successful"

    # Closing the MongoDB session after inserting data.
    client.close()
    return alert