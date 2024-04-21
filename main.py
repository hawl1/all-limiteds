import json
import matplotlib.pyplot as plt

# Read data from JSON file
with open("owners.json", "r") as file:
    data = json.load(file)

# Aggregate counts for each username
user_counts = {}
for item in data.values():
    owners = item.get("owners", [])
    for owner in owners:
        username = owner["name"]
        count = owner["count"]
        user_counts[username] = user_counts.get(username, 0) + count

# Sort user counts by count in descending order
sorted_user_counts = dict(sorted(user_counts.items(), key=lambda item: item[1], reverse=True))

# Create the pie chart
labels = list(sorted_user_counts.keys())
values = list(sorted_user_counts.values())

plt.figure(figsize=(365, 365))
plt.pie(values, labels=labels, autopct='%1.1f%%')
plt.title("Item Ownership Distribution by User")
plt.axis('equal')  # Equal aspect ratio ensures that pie is drawn as a circle.
plt.savefig('item_ownership_distribution.svg')
