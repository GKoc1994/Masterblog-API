"""Masterblog API: a REST API for blog posts built with Flask."""
from flask import Flask, jsonify, request
from flask_cors import CORS
from flask_swagger_ui import get_swaggerui_blueprint

app = Flask(__name__)
CORS(app)  # allow the frontend (other port) to call this API

SWAGGER_URL = "/api/docs"
API_URL = "/static/masterblog.json"
swagger_ui_blueprint = get_swaggerui_blueprint(
    SWAGGER_URL, API_URL, config={"app_name": "Masterblog API"}
)
app.register_blueprint(swagger_ui_blueprint, url_prefix=SWAGGER_URL)

POSTS = [
    {"id": 1, "title": "First post", "content": "This is the first post."},
    {"id": 2, "title": "Second post", "content": "This is the second post."},
]

SORT_FIELDS = ("title", "content")
SORT_DIRECTIONS = ("asc", "desc")


def find_post_by_id(post_id):
    """Return the post with the given id, or None if it does not exist."""
    for post in POSTS:
        if post["id"] == post_id:
            return post
    return None


def next_id():
    """Return a new unique id: one higher than the current highest id."""
    return max((post["id"] for post in POSTS), default=0) + 1


@app.route("/api/posts", methods=["GET"])
def get_posts():
    """
    Return all posts. Optional query parameters:
    sort=title|content and direction=asc|desc.
    """
    sort = request.args.get("sort")
    direction = request.args.get("direction", "asc")

    if sort is None:
        return jsonify(POSTS)
    if sort not in SORT_FIELDS:
        return jsonify({"error": f"Invalid sort field. Use one of {SORT_FIELDS}."}), 400
    if direction not in SORT_DIRECTIONS:
        return jsonify({"error": f"Invalid direction. Use one of {SORT_DIRECTIONS}."}), 400

    sorted_posts = sorted(
        POSTS, key=lambda post: post[sort].lower(), reverse=direction == "desc"
    )
    return jsonify(sorted_posts)


@app.route("/api/posts", methods=["POST"])
def add_post():
    """Add a new post. 'title' and 'content' are required."""
    data = request.get_json(silent=True) or {}
    missing = [field for field in ("title", "content") if not data.get(field)]
    if missing:
        return jsonify({"error": f"Missing field(s): {', '.join(missing)}"}), 400

    new_post = {"id": next_id(), "title": data["title"], "content": data["content"]}
    POSTS.append(new_post)
    return jsonify(new_post), 201


@app.route("/api/posts/<int:post_id>", methods=["DELETE"])
def delete_post(post_id):
    """Delete the post with the given id."""
    post = find_post_by_id(post_id)
    if post is None:
        return jsonify({"error": f"Post with id {post_id} was not found."}), 404

    POSTS.remove(post)
    return jsonify(
        {"message": f"Post with id {post_id} has been deleted successfully."}
    ), 200


@app.route("/api/posts/<int:post_id>", methods=["PUT"])
def update_post(post_id):
    """Update title and/or content. Missing fields keep their old value."""
    post = find_post_by_id(post_id)
    if post is None:
        return jsonify({"error": f"Post with id {post_id} was not found."}), 404

    data = request.get_json(silent=True) or {}
    post["title"] = data.get("title", post["title"])
    post["content"] = data.get("content", post["content"])
    return jsonify(post), 200


@app.route("/api/posts/search", methods=["GET"])
def search_posts():
    """Return posts whose title or content contains the search terms."""
    title = request.args.get("title", "").lower()
    content = request.args.get("content", "").lower()

    results = [
        post for post in POSTS
        if (title and title in post["title"].lower())
        or (content and content in post["content"].lower())
    ]
    return jsonify(results)


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5002, debug=True)
