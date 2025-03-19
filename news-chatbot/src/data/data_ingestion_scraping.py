import requests
from bs4 import BeautifulSoup
import pandas as pd


class BaseNewsScraper:
    def __init__(self, base_url, headers=None):
        self.base_url = base_url
        self.content_classes = ["mosaic m5-m4s", "mosaic m3-3s"]
        self.article_selectors = {
            "link": ["a", "storyblock_title_link"],
            "title": ["a", "storyblock_title_link"],
            "description": ["p", "storyblock_standfirst g_font-body-s"],
            "sub_category": ["a", "storyblock_section g_font-base-s"]
        }

    def fetch_page(self, url):
        """
        Get response from the base url
        """
        try:
            response = requests.get(url, timeout=10)
            response.raise_for_status()
            print(f"...Successfully fetching from {url}")
            return BeautifulSoup(response.content, "html.parser")
        except requests.RequestException as e:
            print(f"...Error fetching {url}: {e}")
            return None

    def scrape_articles(self, soup, url):
        """
        Scrapes articles from the given soup and returns a DataFrame.
        content_classes: List of class names to identify sections containing articles.
        article_selectors: Dictionary with keys 'title', 'link', 'description', and 'category'
        """
        articles_data = []

        for content_class in self.content_classes:
            blocks = soup.find_all("div", class_=content_class)
            for block in blocks:
                articles = block.find_all("article", class_="storyblock")
                if self.base_url == "https://www.skynews.com.au/":
                    category = block.find(
                        "h3", class_="g_font-title-xs").find("a").get_text()
                elif self.base_url == "https://www.news.com.au/":
                    category = url.split("/")[-1]

                for article in articles:

                    data = {
                        "Category": category,
                        "Link": article.find(self.article_selectors['link'][0], class_=self.article_selectors['link'][1])["href"],
                        "Title": article.find(self.article_selectors['title'][0], class_=self.article_selectors['title'][1]).get_text(),
                        "Description": article.find(self.article_selectors['description'][0], class_=self.article_selectors['description'][1]).get_text(),
                        "Sub_category": article.find(self.article_selectors['sub_category'][0], class_=self.article_selectors['sub_category'][1]).get_text()
                    }
                    print(f"...Extracted an article from {self.base_url}")
                    articles_data.append(data)

        return pd.DataFrame(articles_data)

    def get_author_and_date(self, url):
        # Send GET request to the article URL
        response = requests.get(url)

        # If the request was successful, parse the page
        if response.status_code == 200:
            soup = BeautifulSoup(response.content, "html.parser")

            # Extract author name
            author_tag = soup.find("span", class_="author_name")
            if author_tag:
                author = author_tag.get_text(strip=True)
            else:
                author = None  # If not found, set as None

            # Extract the published date
            publish_date_tag = soup.find("div", class_="byline_publish")
            if publish_date_tag:
                publish_date = publish_date_tag.get_text(strip=True)
            else:
                publish_date = None  # If not found, set as None

            return author, publish_date
        else:
            # If request failed, return None for both
            return None, None

    def add_information(self, df):
        # Iterate through the DataFrame and get author and published date for each link
        authors = []
        publish_dates = []

        for index, row in df.iterrows():
            article_url = row['Link']
            print(
                f"exctracting additional information Author and published date...... {article_url}")
            author, publish_date = self.get_author_and_date(article_url)

            # Append the results to the lists
            authors.append(author)
            publish_dates.append(publish_date)

        # Add the author and published date as new columns to the DataFrame
        df['Author'] = authors
        df['Published_Date'] = publish_dates
        return df


class SkyNewsScraper(BaseNewsScraper):
    def __init__(self):
        super().__init__("https://www.skynews.com.au/")

    def scrape(self):
        print(f"Fetching data ...... {self.base_url}")
        soup = self.fetch_page(self.base_url)
        print(f"exctracting article in Tabular format...... {self.base_url}")

        if soup:
            df = self.scrape_articles(soup, self.base_url)
            df = self.add_information(df)

        df.to_csv('news-chatbot/data/raw/news_sky_news.csv', index=False)


class NewsComAuScraper(BaseNewsScraper):
    def __init__(self):
        super().__init__("https://www.news.com.au/")
        self.endpoints = ["national", "world", "lifestyle", "travel",
                          "entertainment", "technology", "finance", "sport"]

    def scrape(self):
        for endpoint in self.endpoints:
            url = self.base_url + endpoint
            print(f"...Fetching data {url}")
            soup = self.fetch_page(url)
            print(f"exctracting article in Tabular format...... {url}")
            if soup:
                df = self.scrape_articles(soup, url)
                df = self.add_information(df)
            df.to_csv(
                f'news-chatbot/data/raw/news_news_{endpoint}.csv', index=False)


if __name__ == "__main__":
    # Sky News Example
    sky_scraper = SkyNewsScraper()
    sky_df = sky_scraper.scrape()

    news_scrapper = NewsComAuScraper()
    news_df = news_scrapper.scrape()
