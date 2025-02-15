import requests
import json
import time
import os

# API URLs
LIST_POSTS_URL = "https://api.supernormal.com/api/v1/posts?scope=latest&date_range=any_time&offset={offset}"
POST_DETAILS_URL = "https://api.supernormal.com/api/v1/posts/{postId}"
TASKS_URL = "https://api.supernormal.com/api/v1/tasks?post_id={postId}&limit=1000"

# Custom User-Agent
HEADERS = {
    "User-Agent": "ThatAPICompanys export script"
}

def get_bearer_token():
    """Prompt the user for a Bearer token and ensure correct formatting."""
    token = input("Enter your Bearer token: ").strip()
    if not token.lower().startswith("bearer "):
        token = f"Bearer {token}"
    return token

def fetch_all_posts(token):
    """Fetch all posts using pagination and return the complete dataset."""
    headers = HEADERS.copy()
    headers["Authorization"] = token

    all_posts = []
    offset = 0

    while True:
        url = LIST_POSTS_URL.format(offset=offset)
        print(f"Fetching posts with offset: {offset}")

        try:
            response = requests.get(url, headers=headers)
            response.raise_for_status()  # Raises an error for HTTP codes 4xx/5xx
            data = response.json()
            
            if not data:  # Stop when no more posts are returned
                print("No more posts found. Stopping pagination.")
                break

            all_posts.extend(data)
            offset += 20  # Move to the next offset

        except requests.exceptions.HTTPError as http_err:
            print(f"HTTP error occurred: {http_err}")
            print("Please check that you have provided the correct token.")
            return None
        except requests.exceptions.RequestException as req_err:
            print(f"Request error: {req_err}")
            return None

    return all_posts

def fetch_post_details(token, post_id):
    """Fetch the full details of a single post using its postId."""
    headers = HEADERS.copy()
    headers["Authorization"] = token
    url = POST_DETAILS_URL.format(postId=post_id)

    try:
        response = requests.get(url, headers=headers)
        response.raise_for_status()
        return response.json()
    except requests.exceptions.HTTPError as http_err:
        print(f"Failed to fetch details for post {post_id}: {http_err}")
    except requests.exceptions.RequestException as req_err:
        print(f"Request error for post {post_id}: {req_err}")

    return None

def fetch_tasks(token, post_id):
    """Fetch tasks for a given post and return the data."""
    headers = HEADERS.copy()
    headers["Authorization"] = token
    url = TASKS_URL.format(postId=post_id)

    try:
        response = requests.get(url, headers=headers)
        response.raise_for_status()
        return response.json()
    except requests.exceptions.HTTPError as http_err:
        print(f"Failed to fetch tasks for post {post_id}: {http_err}")
    except requests.exceptions.RequestException as req_err:
        print(f"Request error for tasks of post {post_id}: {req_err}")

    return None

def save_response_data(data):
    """Save the API response data to a local JSON file with a timestamped filename."""
    timestamp = int(time.time())
    filename = f"posts.json"

    with open(filename, "w") as file:
        json.dump(data, file, indent=4)
    
    print(f"All posts list saved to {filename}")

def save_post_details(post_id, data):
    """Save full post details into a JSON file named after the post ID."""
    os.makedirs("posts", exist_ok=True)  # Ensure the 'posts' directory exists
    filename = os.path.join("posts", f"{post_id}.json")

    with open(filename, "w") as file:
        json.dump(data, file, indent=4)

    print(f"Post {post_id} saved to {filename}")

def save_tasks(post_id, data):
    """Save tasks into a JSON file named after the post ID inside the 'tasks' folder."""
    os.makedirs("tasks", exist_ok=True)  # Ensure the 'tasks' directory exists
    filename = os.path.join("tasks", f"{post_id}.json")

    with open(filename, "w") as file:
        json.dump(data, file, indent=4)

    print(f"Tasks for post {post_id} saved to {filename}")

if __name__ == "__main__":
    token = get_bearer_token()
    posts = fetch_all_posts(token)

    if posts:
        save_response_data(posts)

        # Fetch and save full post details & tasks
        for post in posts:
            post_id = post.get("id")
            if post_id:
                # Fetch post details
                post_details = fetch_post_details(token, post_id)
                if post_details:
                    save_post_details(post_id, post_details)

                # Fetch post tasks
                tasks = fetch_tasks(token, post_id)
                if tasks:
                    save_tasks(post_id, tasks)
