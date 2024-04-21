import json
import matplotlib.pyplot as plt

def generate_pie_chart(user_counts, title, filename):
    # Create the pie chart
    labels = list(user_counts.keys())
    values = list(user_counts.values())

    # Determine the figsize based on the length of users
    num_users = len(labels)
    figsize = (num_users * 0.5, num_users * 0.5)  # Adjust multiplier for desired size

    plt.figure(figsize=figsize)
    plt.pie(values, labels=labels, autopct='%1.1f%%')
    plt.title(title)
    plt.axis('equal')  # Equal aspect ratio ensures that pie is drawn as a circle.
    plt.savefig(filename)

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

# Take top 10 users
top_users = dict(list(sorted_user_counts.items())[:10])

# Generate pie chart for top 10 users
generate_pie_chart(top_users, "Top 10 Item Ownership Distribution by User", "top_10_item_ownership_distribution.svg")

# Generate pie chart for all users
generate_pie_chart(sorted_user_counts, "Item Ownership Distribution by User", "item_ownership_distribution.svg")
