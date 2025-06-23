from flask import Flask, request, jsonify

app = Flask(__name__)

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

if __name__ == "__main__":
    import os
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
