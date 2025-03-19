import pandas as pd
import re
import os
import glob
from textacy import preprocessing


class DataPreprocessingPipeline:
    def __init__(self, directory):
        self.directory = directory
        self.combined_df = None

    def load_data(self):

        csv_files = glob.glob(os.path.join(self.directory, '*.csv'))
        dfs = []
        for file in csv_files:
            print(f"Reading {file}...")
            df = pd.read_csv(file)
            dfs.append(df)

        # Concatenate all DataFrames into one
        self.combined_df = pd.concat(dfs, ignore_index=True)
        self.combined_df.to_csv(os.path.join(
            "news-chatbot/data/interim", 'all_news_combined.csv'), index=False)
        print("All CSVs have been combined into all_news_combined.csv and stored in the interim folder.")

    def clean_author_column(self):

        remove_list = [
            "Lifestyle Reporter", "Digital Reporter", "Business Reporter", "Asia Correspondent",
            "SkyNews.com.au Contributor and Political Commentator", "New York Post", "The Sun",
            "Page Six", "-", " –"
        ]
        pattern = '|'.join(map(re.escape, remove_list))
        self.combined_df["Author"] = self.combined_df["Author"].str.replace(
            pattern, '', regex=True)
        self.combined_df["Author"] = self.combined_df["Author"].str.strip()

    def convert_publish_date(self):

        self.combined_df['Published_Date_con'] = pd.to_datetime(
            self.combined_df['Published_Date'], errors='coerce')
        if pd.api.types.is_datetime64_any_dtype(self.combined_df['Published_Date_con']):
            self.combined_df['Published_Date_con'] = self.combined_df['Published_Date_con'].dt.strftime(
                '%Y-%m-%d %H:%M:%S')
        print(self.combined_df["Published_Date_con"])

    def standardize_category(self):

        self.combined_df['Category'] = self.combined_df['Category'].str.lower()
        self.combined_df['Category'] = self.combined_df['Category'].replace(
            {'local': 'national', 'australia': 'national'})

    def check_https(self):

        self.combined_df['is_https'] = self.combined_df['Link'].apply(
            lambda x: x.startswith('https'))
        any_false = (self.combined_df['is_https'] == False).sum()
        print(f"Any 'False' values in 'is_https' column: {any_false}")

    def preprocess_description(self):

        print("Changing data in 'Description' column to lower case...")
        self.combined_df['Description'] = self.combined_df['Description'].str.lower()
        self.combined_df['length_description'] = self.combined_df['Description'].apply(
            lambda x: len(str(x)))

        # Remove HTML tags
        print("Removing HTML tags from 'Description'...")
        self.combined_df['Description'] = self.combined_df['Description'].apply(
            preprocessing.remove.html_tags)

        # Removing punctuation and brackets
        print("Removing punctuation and brackets from 'Description'...")
        self.combined_df['Description'] = self.combined_df['Description'].apply(
            preprocessing.remove.punctuation)

    def run_pipeline(self):
        """Run all preprocessing steps."""
        self.load_data()
        self.combined_df = pd.read_csv(
            "news-chatbot/data/interim/all_news_combined.csv")
        self.clean_author_column()
        self.convert_publish_date()
        self.standardize_category()
        self.check_https()
        self.preprocess_description()
        self.combined_df.to_csv(os.path.join(
            "news-chatbot/data/processed", 'processed_news.csv'), index=False)
        print("all_news_combined.csv is processed, cleaned and stored in the processed folder.")


# Entry point for the script
if __name__ == "__main__":

    directory = "news-chatbot/data/raw"
    pipeline = DataPreprocessingPipeline(directory)
    pipeline.run_pipeline()
