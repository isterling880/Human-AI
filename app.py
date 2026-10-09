from flask import Flask, jsonify, render_template, request

# Initialize the Flask application
app = Flask(__name__)

# In-memory database / message queue
# In a real production app, you'd replace this with SQLite or PostgreSQL
message_queue = []
next_id = 1

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/admin")
def admin():
    return render_template("admin.html")

@app.route("/api/send", methods=["POST"])
def send_message():
    global next_id
    data = request.get_json()
    user_text = data.get("message", "").strip()
    
    if not user_text:
        return jsonify({"error": "Empty message"}), 400

    # Create a new message entry for the human queue
    new_item = {
        "id": next_id,
        "user_text": user_text,
        "reply_text": None,
        "timestamp": "Just now"
    }
    message_queue.append(new_item)
    next_id += 1
    
    return jsonify({"status": "queued", "id": new_item["id"]})

@app.route("/api/admin/queue", methods=["GET"])
def get_queue():
    return jsonify(message_queue)

@app.route("/api/admin/reply", methods=["POST"])
def submit_reply():
    data = request.get_json()
    msg_id = data.get("id")
    reply_text = data.get("reply", "").strip()

    for item in message_queue:
        if item["id"] == msg_id:
            item["reply_text"] = reply_text
            return jsonify({"status": "success"})

    return jsonify({"error": "Message ID not found"}), 404

@app.route("/api/check/<int:msg_id>", methods=["GET"])
def check_reply(msg_id):
    for item in message_queue:
        if item["id"] == msg_id:
            return jsonify({
                "replied": item["reply_text"] is not None,
                "reply": item["reply_text"]
            })
    return jsonify({"error": "Not found"}), 404

if __name__ == "__main__":
    # Run the local Flask server on port 5000
    app.run(debug=True, port=5000)
