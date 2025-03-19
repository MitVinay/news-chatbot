import requests
from dotenv import load_dotenv
import os
import pandas as pd


class NewsFetcher:
    def __init__(self, access_key):
        self.access_key = access_key
        self.base_url = 'http://api.mediastack.com/v1/news'

    def fetch_news(self):
        # Prepare the parameters for the request
        params = {
            'access_key': self.access_key,
            'countries': 'au,-us',
            'limit': 100,
        }

        # Send the GET request to the Mediastack API
        response = requests.get(self.base_url, params=params)

        # Check if the response is successful
        if response.status_code == 200:
            data = response.json()
            return data
        else:
            raise Exception(f"Failed to fetch data: {response.status_code}")

    def save_news_to_csv(self, data, filename):
        # Create a list to hold the rows
        rows = []

        # Iterate over the 'data' and store each record in the rows list
        for each in data['data']:
            category = each["category"]
            link = each["url"]
            # Assuming the "title" key is present in the data
            title = each["title"]
            description = each["description"]
            sub_category = each["category"]
            author = each["author"]
            published_date = each["published_at"]

            # Append the record to the rows list
            rows.append([category, link, title, description,
                        sub_category, author, published_date])

        # Create a DataFrame from the rows list
        df = pd.DataFrame(rows, columns=[
                          "Category", "Link", "Title", "Description", "Sub_category", "Author", "Published Date"])

        # Write the DataFrame to a CSV file
        df.to_csv(filename, index=False)
        print(f"Data saved to {filename}")


# Usage
if __name__ == "__main__":

    load_dotenv()
    access_key = os.getenv('ACCESS_KEY')
    print(access_key)

    # Initialize the NewsFetcher class with the access key
    fetcher = NewsFetcher(access_key)

    # Fetch news data
    try:
        news_data = fetcher.fetch_news()

        # Save news data to CSV
        fetcher.save_news_to_csv(
            news_data, 'news-chatbot/data/raw/news_mediastack.csv')

    except Exception as e:
        print(f"An error occurred: {e}")
