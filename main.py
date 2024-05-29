import json
import matplotlib.pyplot as plt
import gc

def generate_pie_chart(user_counts, title, filename):
    labels = list(user_counts.keys())
    values = list(user_counts.values())
    num_users = len(labels)
    figsize = (num_users * 0.3, num_users * 0.3)
    plt.figure(figsize=figsize)
    plt.pie(values, labels=labels, autopct='%1.1f%%')
    plt.title(title)
    plt.axis('equal')
    plt.savefig(filename)
    plt.close()
    gc.collect()  # Clear memory

def generate_bar_chart(user_counts, title, filename, num_users):
    plt.figure(figsize=(num_users * 0.4, 4))
    plt.bar(user_counts.keys(), user_counts.values())
    plt.xlabel('Users')
    plt.ylabel('Number of Owned Items')
    plt.title(title)
    plt.xticks(rotation=45, ha='right')
    plt.tight_layout()
    plt.savefig(filename)
    plt.close()
    gc.collect()  # Clear memory

def process_data(file_path):
    user_counts = {}
    with open(file_path, "r") as file:
        data = json.load(file)
        for item in data.values():
            owners = item.get("owners", [])
            for owner in owners:
                username = owner["name"]
                count = owner["count"]
                user_counts[username] = user_counts.get(username, 0) + count
    return user_counts

# Process the data
user_counts = process_data("owners.json")

# Sort users by the number of items in descending order
sorted_user_counts = dict(sorted(user_counts.items(), key=lambda item: item[1], reverse=True))

# Get the top 10 users with the most items
top_users = dict(list(sorted_user_counts.items())[:10])

# Generate a pie chart for the top 10 users
generate_pie_chart(top_users, "Top 10 Item Ownership Distribution by User", "top_10_item_ownership_distribution.svg")

# Generate a bar chart for the top 10 users
generate_bar_chart(top_users, "Top 10 Item Ownership Distribution by User", "top_10_item_ownership_distribution_bar.svg", len(top_users))

# Generate a pie chart for all users
generate_pie_chart(sorted_user_counts, "Item Ownership Distribution by User", "item_ownership_distribution.svg")

# Generate a bar chart for all users
generate_bar_chart(sorted_user_counts, "Item Ownership Distribution by User", "item_ownership_distribution_bar.svg", len(sorted_user_counts))

# Aggregate counts for each username using a generator
def aggregate_user_counts(data):
    user_counts = {}
    for item in data:
        owners = item.get("owners", [])
        for owner in owners:
            username = owner["name"]
            count = owner["count"]
            user_counts[username] = user_counts.get(username, 0) + count
    return user_counts

# Process data using generators
user_counts = aggregate_user_counts(read_json_data("owners.json"))

# Generate pie chart for top 10 users
top_users = dict(sorted(user_counts.items(), key=lambda item: item[1], reverse=True)[:10])
generate_pie_chart(top_users, "Top 10 Item Ownership Distribution by User", "top_10_item_ownership_distribution.svg")

# Generate bar chart for top 10 users
generate_bar_chart(top_users, "Top 10 Item Ownership Distribution by User", "top_10_item_ownership_distribution_bar.svg", len(top_users))

# Generate pie chart for all users
generate_pie_chart(user_counts, "Item Ownership Distribution by User", "item_ownership_distribution.svg")

# Generate bar chart for all users
generate_bar_chart(user_counts, "Item Ownership Distribution by User", "item_ownership_distribution_bar.svg", len(user_counts))
