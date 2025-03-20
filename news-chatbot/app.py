from flask import Flask, render_template, request
from src.highlights import Highlights

app = Flask(__name__)

# Sample news data
news_items = [
    {
        'title': 'Market Trends 2024',
        'category': 'business',
        'author': 'John Doe',
        'source': 'Financial Times',
        'frequency': 'High',
        'published': '2024-03-20'
    },
    {
        'title': 'AI Innovations',
        'category': 'tech',
        'author': 'Jane Smith',
        'source': 'TechCrunch',
        'frequency': 'Trending',
        'published': '2024-03-19'
    }
]


@app.route('/')
def index():
    category = request.args.get('category', 'all')

    if category == 'all':
        filtered_news = news_items
    else:
        filtered_news = [item for item in news_items
                         if item['category'] == category]

    return render_template('index.html',
                           news=filtered_news,
                           current_category=category)


if __name__ == '__main__':
    app.run(debug=True)
