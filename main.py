import json
import matplotlib.pyplot as plt

def generate_pie_chart(user_counts, title, filename):
    labels = list(user_counts.keys())
    values = list(user_counts.values())
    num_users = len(labels)
    plt.figure()
    plt.pie(values, labels=labels, autopct='%1.1f%%')
    plt.title(title)
    plt.axis('equal')
    plt.tight_layout()
    plt.savefig(filename)
    plt.close()

def generate_bar_chart(user_counts, title, filename, num_users):
    plt.figure()
    plt.bar(user_counts.keys(), user_counts.values())
    plt.xlabel('Users')
    plt.ylabel('Number of Owned Items')
    plt.title(title)
    plt.xticks(rotation=45, ha='right')
    plt.tight_layout()
    plt.savefig(filename)
    plt.close()

def aggregate_others(user_counts, top_count):
    total_count = sum(user_counts.values())
    if len(user_counts) <= top_count:
        return user_counts
    else:
        top_users = dict(list(user_counts.items())[:top_count])
        other_count = total_count - sum(top_users.values())
        top_users["Others"] = other_count
        return top_users

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

# Aggregate other users into "others" category
top_users_with_others = aggregate_others(sorted_user_counts, 10)

# Generate a pie chart for the top 10 users including "others"
generate_pie_chart(top_users_with_others, "Top 10 Item Ownership Distribution by User", "top_10_item_ownership_distribution.svg")

# Generate a bar chart for the top 10 users
generate_bar_chart(top_users, "Top 10 Item Ownership Distribution by User", "top_10_item_ownership_distribution_bar.svg", len(top_users))