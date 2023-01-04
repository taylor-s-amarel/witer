import requests
import re
import os
from datetime import datetime, timedelta

# Set the subreddit and time period to scrape
subreddit = 'combatfootage'
days_ago = 7

# Get the current time and calculate the time `days_ago` days ago
now = datetime.utcnow()
before = now - timedelta(days=days_ago)

# Convert the timestamp to the format that Reddit uses
before = before.strftime('%Y-%m-%dT%H:%M:%S.%f')[:-3] + 'Z'

# Set the user agent to avoid being blocked by Reddit
headers = {'User-Agent': 'Mozilla/5.0'}

# Set the URL to get the newest submissions from `subreddit`
url = f'https://www.reddit.com/r/{subreddit}/new/.json?sort=new&before={before}'

# Make the request
res = requests.get(url, headers=headers)

# Get the JSON data from the response
data = res.json()

# Extract the URLs of the gifs and videos
gifs_and_videos = [
    post['data']['url']
    for post in data['data']['children']
    if post['data']['url'].endswith(('.gif', '.mp4'))
]

# Create a directory to store the gifs and videos
if not os.path.exists(subreddit):
    os.makedirs(subreddit)

# Download each gif and video
for url in gifs_and_videos:
    # Get the file name from the URL
    file_name = re.search(r'/(\w+\.\w+)$', url)[1]
    file_path = f'{subreddit}/{file_name}'
    
    # Download the file
    with open(file_path, 'wb') as f:
        f.write(requests.get(url).content)

print(f'Downloaded {len(gifs_and_videos)} gifs and videos from r/{subreddit}')
