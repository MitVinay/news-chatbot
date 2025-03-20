from flask import Flask, render_template, request
from src.highlights import Highlights

app = Flask(__name__)

checker = Highlights()
news_highlight = checker.get_highlights()

print(".....Fetching the highlighted news")


@app.route('/home')
def index():
    category = request.args.getlist('category')
    print(category)
    all_data = []
    for cat, data in checker.category_documents.items():
        if cat in category:
            all_data.extend(data)
    # If no categories are selected, use 'all' as the default
    if not category:
        category = ['all']

    if category == 'all':
        all_data = [item for sublist in checker.category_documents.values()
                    for item in sublist]

    return render_template('index.html',
                           news=all_data,
                           highlighted_news=news_highlight,
                           current_category=category)


if __name__ == '__main__':
    app.run(debug=True)
