import requests

# Replace these with actual values
api_url = "http://3.129.20.16:8000/api/v1/news"
#JWT token changes every time so please generate token and use it


# Replace this with the actual technology_name you want to filter by
# technology_name = "AI"

url = f"{api_url}"

response = requests.get(api_url)

if response.status_code == 200:
    news_data = response.json()
    # Process the news_data as needed
    results = news_data.get("results", [])
    for news_item in results:
        print(news_item)
else:
    print(f"Failed to retrieve data. Status code: {response.status_code}")