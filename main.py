import json
import plotly.graph_objects as go

def generate_pie_chart(user_counts, title, filename):
    labels = list(user_counts.keys())
    values = list(user_counts.values())

    fig = go.Figure(data=[go.Pie(labels=labels, values=values)])
    fig.update_layout(title=title)
    fig.write_image(filename, format="svg")

def generate_bar_chart(user_counts, title, filename):
    fig = go.Figure([go.Bar(x=list(user_counts.keys()), y=list(user_counts.values()))])
    fig.update_layout(title=title, xaxis=dict(tickangle=45))
    fig.write_image(filename, format="svg")

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
generate_pie_chart(top_users, "Top 10 Item Ownership Distribution by User", "top_10_item_ownership_distribution_plotly.svg")

# Generate bar chart for top 10 users
generate_bar_chart(top_users, "Top 10 Item Ownership Distribution by User", "top_10_item_ownership_distribution_bar_plotly.svg")

# Generate pie chart for all users
generate_pie_chart(sorted_user_counts, "Item Ownership Distribution by User", "item_ownership_distribution_plotly.svg")

# Generate bar chart for all users
generate_bar_chart(sorted_user_counts, "Item Ownership Distribution by User", "item_ownership_distribution_bar_plotly.svg")
