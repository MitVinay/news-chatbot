# news-chatbot

<a target="_blank" href="https://cookiecutter-data-science.drivendata.org/">
    <img src="https://img.shields.io/badge/CCDS-Project%20template-328F97?logo=cookiecutter" />
</a>

I-powered system that extracts news articles from multiple Australian news outlets, categorizes and summarizes them, and then presents daily highlights in a user-friendly UI. Additionally, a chatbot should be implemented to allow users to ask questions about the highlights using Retrieval-Augmented Generation (RAG).

## Project Organization

```
├── LICENSE            <- Open-source license if one is chosen
├── Makefile           <- Makefile with convenience commands like `make data` or `make train`
├── README.md          <- The top-level README for developers using this project.
├── data
│   ├── interim        <- Intermediate data that has been transformed.
│   ├── processed      <- The final, canonical data sets for modeling.
│   └── raw            <- The original, immutable data dump.
│
│
├── models             <- Trained and serialized models, model predictions, or model summaries
│
├── notebooks          <- Jupyter notebooks. Naming convention is a number (for ordering),
│   │                  the creator's initials, and a short `-` delimited description, e.g.
│   │                      `1.0-jqp-initial-data-exploration`.
│   │
│   ├── data_exploration_preprocessing.ipynb <- Code to explore the data>
│   ├── data_storing_sample_code.ipynb          <- Sample code to store the data>
│   ├── model_breaking_news_clasifier.ipynb     <- Code to build a classfier>
│   └── similar_news.ipynb                      <- Find the similar news>
│
│
│
│
├── database < Contain chromadb vectore database>
│
│
├── static/images/    < Contains images for the website>
│
│
└── templates   <- Contains the templates for the project
│    │
│   ├── index.html
│
│
│
├── reports            <- Detailed Report of the thought process and application planning
│
│
├── requirements.txt   <- The requirements file for reproducing the analysis environment, e.g.
│                         generated with `pipenv requirements > news-chatbot/requirements.txt`
│
│
└── app.py  < Flask application>
│
│
└── src   <- Source code for use in this project.
    │
    ├── __init__.py             <- Makes news_chatbot a Python module
    │
    ├── highlights.py               <- Code to generate the highlights of the news
    │
    ├── data
    │   ├── data_ingestion_api.py          <- Code to extract data through APIs
    │   └── data_ingestion_rss_feed.py      <- Code to extract data through rss_fee
    │   └── data_ingestion_scraping.py      <- Code to extract data through scraping
    │   └── data_preprocessing.py           <- Perform the data cleaning and preprocessing
    │   └── chroma_data_pipeline.py            <- Code to store data in chroma db
    │
    └── plots.py                <- Code to create visualizations
```

---
