import json

# Replace 'your_file_path.json' with the actual path to your JSON file
file_path = 'review_data_1.json'

# Open the JSON file and load its content
with open(file_path, 'r') as json_file:
    data = json.load(json_file)

# Check the length of the JSON data (assuming it's a list or a dictionary)
item_count = len(data)

# Print the number of items
print("Number of items in the JSON file:", item_count)