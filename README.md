# Literature Relevance API

This is a simple Flask API to simulate searching and evaluating the relevance of academic articles to a given topic.

## Endpoints

- `GET /articles/search?topic=your_query&limit=5`
- `POST /articles/evaluate` with JSON body:

```json
{
  "topic": "phenomenal consciousness",
  "articles": [
    {
      "title": "Some Article",
      "authors": "Author Name",
      "year": 2022,
      "abstract": "Text here...",
      "url": "https://..."
    }
  ]
}
```

## Running locally

```bash
pip install -r requirements.txt
python app.py
```
