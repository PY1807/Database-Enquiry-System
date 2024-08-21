import re
import json
from pymongo import MongoClient
from bson import json_util
from .App import give_query

# Establish a connection to MongoDB
client = MongoClient('mongodb://localhost:27017/')  # Update with your MongoDB connection details
db = client['Client_Management']  # Replace 'Client_Management' with your database name
collection = db['Client']  # Replace 'Login_details' with your collection name

def extract_query(message):
    # Define a regex pattern to find the part of the message containing a MongoDB operation
    pattern = r"person\.(find|aggregate|update|insert|delete|findOne)\((\{.*?\}(, \{.*?\})?)\)"
    
    # Search for the pattern in the message
    match = re.search(pattern, message, re.DOTALL)
    
    if match:
        # Return the matched query type and query string
        return match.group(1), match.group(2)
    return None, None

def handlequery(query):
    query_result = None
    query_to_execute = give_query(query)
    print(query_to_execute)
    
    query_type, query2 = extract_query(query_to_execute)
    print(f"Query Type: {query_type}")
    print(f"Query: {query2}")
    
    # Execute the query
    try:
        if query_type == 'find':
            filter_str, projection_str = re.findall(r'\{.*?\}', query2)
            filter_dict = json.loads(filter_str)
            projection_dict = json.loads(projection_str)
            query_result = collection.find(filter_dict, projection_dict)
        elif query_type == 'aggregate':
            pipeline_str = query2
            pipeline = json_util.loads(pipeline_str)
            query_result = collection.aggregate(pipeline)
        elif query_type == 'update':
            filter_str, update_str = re.findall(r'\{.*?\}', query2)
            filter_dict = json.loads(filter_str)
            update_dict = json.loads(update_str)
            query_result = collection.update_one(filter_dict, update_dict)
        elif query_type == 'insert':
            document_str = query2
            document_dict = json.loads(document_str)
            query_result = collection.insert_one(document_dict)
        elif query_type == 'delete':
            filter_str = query2
            filter_dict = json.loads(filter_str)
            query_result = collection.delete_one(filter_dict)
        elif query_type == 'findOne':
            filter_str = query2
            filter_dict = json.loads(filter_str)
            query_result = collection.find_one(filter_dict)
        else:
            print("No valid query found")
        
        print(query_result)
        print(type(query_result))

        # Convert cursor to list to return data
        if isinstance(query_result, type(collection.find())):  # If the result is a cursor
            query_result = list(query_result)
        elif isinstance(query_result, type(collection.aggregate([]))):  # If the result is an aggregate cursor
            query_result = list(query_result)

    except Exception as e:
        print(f"Error executing query: {e}")

    return query_result if query_result is not None else []

def serialize_mongo_documents(documents):
    if documents:
        return json_util.dumps(documents)
    return "[]"  # Return empty JSON array if documents is None or empty









