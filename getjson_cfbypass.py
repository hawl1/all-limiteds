import re
import requests
import time
import json

items = {}

def fetch_items(page=1):
    """Fetch a page of items."""
    url = f"https://polytoria.com/api/store/items?types[]=tool&types[]=face&types[]=hat&page={page}&search=&sort=createdAt&order=desc&showOffsale=false&collectiblesOnly=true"
    headers = {"Content-Type": "application/json"}
    data = {
        "cmd": "request.get",
        "url": url,
        "maxTimeout": 60000
    }
    response = requests.post("http://localhost:20080/v1", headers = headers, json = data)
    response = response.json()["solution"]["response"]
    response = re.sub(r'<.*?>', '', response)
    return response

def fetch_owners(item_id, page=1):
    """Fetch a page of items."""
    url = f"https://api.polytoria.com/v1/store/{item_id}/owners?limit=100&page={page}"
    headers = {"Content-Type": "application/json"}
    data = {
        "cmd": "request.get",
        "url": url,
        "maxTimeout": 60000
    }
    response = requests.post("http://localhost:20080/v1", headers = headers, json = data)
    response = response.json()["solution"]["response"]
    response = re.sub(r'<.*?>', '', response)
    return response

def process_all_items():
    """Fetch all items and process each one."""
    page = 1
    while True:
        response = fetch_items(page)
        try:
            json_response = json.loads(response)
        except json.JSONDecodeError:
            print(f"Error parsing JSON for page {page}. Waiting...")
            time.sleep(10)  # Wait for 10 seconds and try again
            continue  # Retry fetching the page
        for item in json_response['data']:
            item_id = item['id']
            item_name = item['name']
            items[item_id] = {'name': item_name, 'owners': []}
            process_owners(item_id)
        if page >= json_response['meta']['lastPage']:
            break
        page += 1
        time.sleep(0.6)

def process_owners(item_id):
    """Fetch all pages of owner data for a given item and update the items dictionary."""
    page = 1
    while True:
        response = fetch_owners(item_id, page)
        # response = handle_rate_limit(response)  # Handle rate limit before processing
        try:
            json_response = json.loads(response)
        except json.JSONDecodeError:
            print(f"Error parsing JSON for item {item_id}, page {page}. Waiting...")
            time.sleep(10)  # Wait for 10 seconds and try again
            continue  # Retry fetching the page
        if not json_response['inventories']:
            break
        for inventory in json_response['inventories']:
            username = inventory['user']['username']
            # Find owner in the list or add new
            found = False
            for owner in items[item_id]['owners']:
                if owner['name'] == username:
                    owner['count'] += 1
                    found = True
                    break
            if not found:
                items[item_id]['owners'].append({'name': username, 'count': 1})
        if json_response['pages'] == page:
            break
        page += 1
        time.sleep(0.6)

def main():
    process_all_items()
    with open('owners.json', 'w') as file:
        json.dump(items, file, indent=4)

if __name__ == "__main__":
    main()
