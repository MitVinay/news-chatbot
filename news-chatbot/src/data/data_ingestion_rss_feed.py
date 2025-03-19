import feedparser
import pandas as pd
import ssl
import os
import certifi


class RSSFeedParser:
    def __init__(self, rss_urls, output_folder: str = 'news-chatbot/data/raw/'):

        self.rss_urls = rss_urls
        self.output_folder = output_folder

    def parse_rss_feed(self, rss_url: str):

        try:
            # Parse the RSS feed
            feed = feedparser.parse(rss_url)
            category = rss_url.split("/")[-1]
            os.environ['SSL_CERT_FILE'] = certifi.where()

            if hasattr(ssl, '_create_unverified_context'):
                ssl._create_default_https_context = ssl._create_unverified_context

            # Return a list of articles as dictionaries
            return [{
                "Category": category,
                "Link": entry.link,
                "Title": entry.title,
                "Description": entry.summary,
                "Sub_category": ', '.join(tag['term'] for tag in entry.get('tags', [])) or category,
                "Author": entry.get('author', '9news.com'),
                "Published_Date": entry.published if 'published' in entry else "Unknown"
            } for entry in feed.entries]

        except Exception as e:
            print(f"Error parsing RSS feed from {rss_url}: {e}")
            return None

    def save_to_csv(self, df: pd.DataFrame, category: str) -> None:

        df.to_csv(f'{self.output_folder}news_9news_{category}.csv', index=False)
        print(f"Saved {category} data to CSV.")

    def process_feeds(self):

        for rss_url in self.rss_urls:
            print(f"Processing {rss_url}...")

            # Parse the RSS feed and get the articles
            articles = self.parse_rss_feed(rss_url)

            # Convert articles to DataFrame
            df = pd.DataFrame(articles)

            # Save DataFrame to CSV
            category = rss_url.split("/")[-1]
            if df is not None:
                self.save_to_csv(df, category)


# Main function to execute the logic
def main():
    rss_urls = [
        "https://www.9news.com/feeds/syndication/rss/sports",
        "https://www.9news.com/feeds/syndication/rss/news/local",
        "https://www.9news.com/feeds/syndication/rss/news/entertainment-news",
        "https://www.9news.com/feeds/syndication/rss/news/politics",
        "https://www.9news.com/feeds/syndication/rss/news/investigations"
    ]

    # Create an instance of the RSSFeedParser class
    rss_parser = RSSFeedParser(rss_urls)

    # Process the feeds and save them to CSV
    rss_parser.process_feeds()


# Entry point for the script
if __name__ == "__main__":
    main()
