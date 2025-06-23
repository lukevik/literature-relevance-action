from flask import Flask, request, jsonify

from flask import Flask, request, jsonify, send_from_directory
import os

app = Flask(__name__)

@app.route("/", methods=["GET"])
def home():
    return "✅ Literature Relevance API is running."

@app.route("/.well-known/openapi.yaml", methods=["GET"])
def serve_openapi_spec():
    return send_from_directory(directory=".well-known", path="openapi.yaml", mimetype="text/yaml")


# Simulated database of articles
mock_articles = [
    {
        "title": "Phenomenal Consciousness and the Explanatory Gap",
        "authors": "J. Levine",
        "year": 2021,
        "abstract": "This paper revisits the explanatory gap between physical processes and phenomenal experience.",
        "url": "https://example.com/phenomenal-consciousness"
    },
    {
        "title": "The Case for Non-reductive Physicalism",
        "authors": "K. Wilson",
        "year": 2020,
        "abstract": "Argues that physicalism does not require reductionism.",
        "url": "https://example.com/non-reductive"
    }
]

@app.route("/articles/search", methods=["GET"])
def search_articles():
    topic = request.args.get("topic", "")
    limit = int(request.args.get("limit", 5))
    results = [a for a in mock_articles if topic.lower() in a["title"].lower() or topic.lower() in a["abstract"].lower()]
    return jsonify(results[:limit])

@app.route("/articles/evaluate", methods=["POST"])
def evaluate_articles():
    data = request.get_json()
    topic = data.get("topic", "").lower()
    articles = data.get("articles", [])
    evaluations = []

    for article in articles:
        score = 0.0
        if topic in article["title"].lower():
            score += 0.6
        if topic in article["abstract"].lower():
            score += 0.4
        evaluations.append({
            "title": article["title"],
            "relevance_score": round(score, 2),
            "summary": article["abstract"][:120] + "...",
            "justification": "High match in title." if score > 0.6 else "Partial match in abstract."
        })

    return jsonify({"evaluations": evaluations})
@app.route("/topics", methods=["GET"])
def list_topics():
    return jsonify([
        "phenomenal consciousness",
        "non-reductive physicalism",
        "dualism",
        "intentionality",
        "free will",
        "mental causation"
    ])

@app.route("/articles/summarize", methods=["POST"])
def summarize_articles():
    data = request.get_json()
    articles = data.get("articles", [])
    summaries = []

    for article in articles:
        summary = article["abstract"][:120] + "..." if "abstract" in article else ""
        summaries.append({
            "title": article.get("title", "Untitled"),
            "summary": summary
        })

    return jsonify({"summaries": summaries})

@app.route("/articles/<string:title>", methods=["GET"])
def get_article_by_title(title):
    match = next((a for a in mock_articles if a["title"].lower() == title.lower()), None)
    if match:
        return jsonify(match)
    else:
        return jsonify({"error": "Article not found"}), 404

if __name__ == "__main__":
    import os
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
