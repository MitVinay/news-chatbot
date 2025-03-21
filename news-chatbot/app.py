from flask import Flask, render_template, request
from src.highlights import Highlights
import chromadb
import os
from dotenv import load_dotenv
from openai import OpenAI
from sentence_transformers import SentenceTransformer
import chromadb


app = Flask(__name__)

checker = Highlights()
news_highlight = checker.get_highlights()

print(".....Fetching the highlighted news")
EMBEDDING_MODEL = "sentence-transformers/all-MiniLM-L6-v2"
embedding_model = SentenceTransformer(EMBEDDING_MODEL)


@app.route('/')
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
    print(all_data)

    return render_template('index.html',
                           news=all_data,
                           highlighted_news=news_highlight,
                           current_category=category)


@app.route('/chat', methods=['POST'])
def chat_endpoint():
    category = request.args.getlist('category')
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
    print(all_data)
    # Initialize
    load_dotenv()
    openai_api_key = os.getenv('OPENAI_API_KEY')

    openai = OpenAI()
    MODEL = 'gpt-4o-mini'

    system_message = "You are a helpful assistant and respectful assistant"
    message = request.form.get('message')
    print(message)

    # Initialize ChromaDB client
    client = chromadb.PersistentClient(path="news-chatbot/databases/news")
    collection = client.get_or_create_collection("processed_news")

    # Initialize embedding model

    query_embedding = embedding_model.encode([message]).tolist()[0]

    # Query ChromaDB
    results = collection.query(
        query_embeddings=[query_embedding],
        n_results=3,
        include=["metadatas", "documents"]
    )

    # Build context
    context = "\n".join(results['documents'][0])
    full_prompt = f"""Context information:
    {context}
    
    User Question: {message}
    
    Answer based on the context and your knowledge:"""

    # Prepare messages for OpenAI
    messages = [{"role": "system", "content": system_message}] + \
        [{"role": "user", "content": full_prompt}]

    # Generate response
    response = openai.chat.completions.create(
        model=MODEL,
        messages=messages,
        stream=False  # Changed to False for single response
    )

    # Format references
    references = results['metadatas'][0]

    return render_template('index.html',
                           response=response.choices[0].message.content,
                           references=references,
                           message=message,
                           news=all_data,
                           highlighted_news=news_highlight,
                           current_category=category)


if __name__ == '__main__':
    app.run(debug=True)
