import matplotlib.pyplot as plt
from pymongo import MongoClient
from pymongo.server_api import ServerApi

# MongoDB connection URI
uri = "mongodb+srv://allendalangin15:Kl9y8WC05MdEVXC5@database.7fqnq.mongodb.net/?retryWrites=true&w=majority"

# Create a new client and connect to the server
client = MongoClient(uri, server_api=ServerApi('1'))

# Send a ping to confirm a successful connection
try:
    client.admin.command('ping')
    print("Pinged your deployment. You successfully connected to MongoDB!")
except Exception as e:
    print(e)

# Database and collection
db = client.test  # Database name
collection = db.statistics  # Collection name

# Fetch all documents from the collection
data = list(collection.find({}))

# Iterate through each document and plot the data
for document in data:
    # Extract data for plotting
    table_title = document['table_title']
    x_axis_label = document['x_axis_label']
    y_axis_label = document['y_axis_label']
    data_points = document['data_points']

    # Prepare x and y values
    x_values = [point['x'] for point in data_points]
    y_values = [int(point['y']) for point in data_points]  # Convert y values to integers

    # Create a new figure for each plot
    plt.figure(figsize=(10, 5))

    # Plot the data
    plt.plot(x_values, y_values, marker='o', linestyle='-', color='b')

    # Add titles and labels
    plt.title(table_title)
    plt.xlabel(x_axis_label)
    plt.ylabel(y_axis_label)
    plt.grid(True)

    # Rotate x-axis labels for better readability
    plt.xticks(rotation=45)

    # Show the plot
    plt.tight_layout()
    plt.show()