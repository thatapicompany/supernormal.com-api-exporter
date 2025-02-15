# Supernormal API Export Script

This script fetches all posts from the Supernormal API and saves them as a JSON file.

At time of creation there was no support for this via the Official Supernormal API, so this script was created to fill that gap.

We have also intocluded the OpenAPI spec doc we have created by reverse engineering the Supernormal API. This is a work in progress and may not be 100% accurate.

## Author
- [Aden Forshaw - ThatAPICompany.com](https://ThatAPICompany.com)

## **Prerequisites**
To run this script, you need:
- **Python 3** installed (Check with `python --version` or `python3 --version`)
- An **API Bearer token** for authentication - this comes from your Browser after logging into your account

## Running locally via a virtual environment

```
python3 -m pip install --user virtualenv
python3 -m venv env
source env/bin/activate
pip install -r requirements.txt
python3 export_posts.py
```

You will be asked for a Bearer token. Get it from your browser 'network' tab after logging into your Supernormal account and then Paste it in and press enter.

The script will then fetch all posts and save them to a file called `posts.json`. 
All Posts will be saved in a folder called `posts` as individual JSON files, and all the tasks from the posts will be saved in a folder called `tasks` as individual JSON files.

## Finding your Bearer Token

1. Log into your Supernormal account
2. Open the Developer Tools in your browser (usually by pressing F12)
3. Go to the 'Network' tab
4. Refresh the page
5. Look for a request to `api.supernormal.com` in the list of requests - or one called `user`
6. Click on the request and look for the `Authorization` header in the request headers
7. Copy the value of the `Authorization` header (it should start with `Bearer`) and paste it into the script when prompted
