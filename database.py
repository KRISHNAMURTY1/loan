from pymongo import MongoClient
import datetime

# MongoDB connection
client = MongoClient("mongodb+srv://your_mongodb_uri")
db = client["loan_app"]

# Add user to the database
def add_user(user_data, collection_name):
    collection = db[collection_name]
    collection.insert_one(user_data)

# Check if a username already exists
def check_username_exists(username):
    loan_agents = db["loan_agents"]
    loan_receivers = db["loan_receivers"]
    return loan_agents.find_one({"username": username}) or loan_receivers.find_one({"username": username})

# Add a transaction
def add_transaction(data):
    transactions = db["transactions"]
    data["timestamp"] = datetime.datetime.now()
    data["status"] = "pending"  # Default status
    transactions.insert_one(data)

# Get transactions for a user
def get_transactions_by_user(username, role, start_date=None, end_date=None):
    transactions = db["transactions"]
    query = {"receiver": username} if role == "loan_receiver" else {"loan_agent": username}

    if start_date and end_date:
        query["timestamp"] = {"$gte": datetime.datetime.combine(start_date, datetime.time.min),
                              "$lte": datetime.datetime.combine(end_date, datetime.time.max)}

    return list(transactions.find(query))

# Update transaction status
def update_transaction_status(transaction_id, status):
    transactions = db["transactions"]
    transactions.update_one({"_id": transaction_id}, {"$set": {"status": status}})

# Other database operations as needed...
