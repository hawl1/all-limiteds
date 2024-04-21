import json
import matplotlib.pyplot as plt

def generate_pie_chart(user_counts, title, filename):
    # Create the pie chart
    labels = list(user_counts.keys())
    values = list(user_counts.values())

    # Determine the figsize based on the number of users
    num_users = len(labels)
    figsize = (num_users * 0.3, num_users * 0.3)  # Adjust multiplier for desired size

    plt.figure(figsize=figsize)
    plt.pie(values, labels=labels, autopct='%1.1f%%')
    plt.title(title)
    plt.axis('equal')  # Equal aspect ratio ensures that pie is drawn as a circle.
    plt.savefig(filename)  # Save the plot directly to a file
    plt.close()  # Close the plot to release resources

def generate_bar_chart(user_counts, title, filename, num_users):
    # Create the bar chart
    plt.figure(figsize=(num_users * 0.4, 4))
    plt.bar(user_counts.keys(), user_counts.values())
    plt.xlabel('Users')
    plt.ylabel('Number of Owned Items')
    plt.title(title)
    plt.xticks(rotation=45, ha='right')
    plt.tight_layout()
    plt.savefig(filename)  # Save the plot directly to a file
    plt.close()  # Close the plot to release resources

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

# Generate bar chart for top 10 users
generate_bar_chart(top_users, "Top 10 Item Ownership Distribution by User", "top_10_item_ownership_distribution_bar.svg", len(top_users))

# Generate pie chart for all users
generate_pie_chart(sorted_user_counts, "Item Ownership Distribution by User", "item_ownership_distribution.svg")

# Generate bar chart for all users
generate_bar_chart(sorted_user_counts, "Item Ownership Distribution by User", "item_ownership_distribution_bar.svg", len(sorted_user_counts))
