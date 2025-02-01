import re
import requests
import time
import json

items = {}

def fetch_items(page=1):
    """Fetch a page of items with retry logic."""
    max_retries = 5
    retries = 0
    while retries < max_retries:
        try:
            url = f"https://polytoria.com/api/store/items?types[]=tool&types[]=face&types[]=hat&page={page}&search=&sort=createdAt&order=desc&showOffsale=false&collectiblesOnly=true"
            headers = {"Content-Type": "application/json"}
            data = {
                "cmd": "request.get",
                "url": url,
                "maxTimeout": 60000
            }
            response = requests.post("http://localhost:20080/v1", headers=headers, json=data)
            json_data = response.json()
            if 'solution' not in json_data:
                raise KeyError("'solution' key not found in response")
            solution_response = json_data["solution"]["response"]
            cleaned_response = re.sub(r'<.*?>', '', solution_response)
            return cleaned_response
        except (KeyError, json.JSONDecodeError) as e:
            print(f"Error fetching items page {page}: {e}. Retry {retries + 1}/{max_retries} in 10 seconds...")
            retries += 1
            time.sleep(10)
    print(f"Max retries ({max_retries}) reached for items page {page}. Skipping...")
    return None

def fetch_owners(item_id, page=1):
    """Fetch a page of owners with retry logic."""
    max_retries = 7 # it is 7 because mah fav number is 7, 7 11 bitch!
    retries = 0
    while retries < max_retries:
        try:
            url = f"https://api.polytoria.com/v1/store/{item_id}/owners?limit=100&page={page}"
            headers = {"Content-Type": "application/json"}
            data = {
                "cmd": "request.get",
                "url": url,
                "maxTimeout": 60000
            }
            response = requests.post("http://localhost:20080/v1", headers=headers, json=data)
            json_data = response.json()
            if 'solution' not in json_data:
                raise KeyError("'solution' key not found in response")
            solution_response = json_data["solution"]["response"]
            cleaned_response = re.sub(r'<.*?>', '', solution_response)
            return cleaned_response
        except (KeyError, json.JSONDecodeError) as e:
            print(f"Error fetching owners for item {item_id}, page {page}: {e}. Retry {retries + 1}/{max_retries} in 10 seconds...")
            retries += 1
            time.sleep(10)
    print(f"Max retries ({max_retries}) reached for item {item_id}, page {page}. Skipping...")
    return None

def process_all_items():
    """Fetch all items and process each one with error handling."""
    page = 1
    while True:
        response = fetch_items(page)
        if response is None:
            print(f"Skipping page {page} due to fetch failure.")
            page += 1
            continue
        try:
            json_response = json.loads(response)
        except json.JSONDecodeError:
            print(f"Error parsing JSON for page {page}. Waiting...")
            time.sleep(10)
            continue
        if 'data' not in json_response:
            print(f"Invalid data structure in page {page}. Skipping...")
            page += 1
            continue
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
    """Process owners with error handling for failed fetches."""
    page = 1
    while True:
        response = fetch_owners(item_id, page)
        if response is None:
            print(f"Skipping further processing for item {item_id} due to fetch failures.")
            break
        try:
            json_response = json.loads(response)
        except json.JSONDecodeError:
            print(f"Error parsing JSON for item {item_id}, page {page}. Waiting...")
            time.sleep(10)
            continue
        if not json_response.get('inventories', []):
            break
        for inventory in json_response['inventories']:
            username = inventory['user']['username']
            found = False
            for owner in items[item_id]['owners']:
                if owner['name'] == username:
                    owner['count'] += 1
                    found = True
                    break
            if not found:
                items[item_id]['owners'].append({'name': username, 'count': 1})
        if json_response.get('pages', 0) == page:
            break
        page += 1
        time.sleep(0.6)

def main():
    process_all_items()
    with open('owners.json', 'w') as file:
        json.dump(items, file, indent=4)

if __name__ == "__main__":
    main()