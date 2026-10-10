from flask import Flask, render_template, request, jsonify

app = Flask(__name__)

message_queue = []

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/send', methods=['POST'])
def send_message():
    data = request.get_json()
    message_text = data.get('message')
    if message_text:
        message_queue.append({'user': message_text, 'reply': None})
    return jsonify({'status': 'Success'})

@app.route('/admin/queue', methods=['GET'])
def get_queue():
    return jsonify(message_queue)

@app.route('/admin/reply', methods=['POST'])
def admin_reply():
    data = request.get_json()
    index = data.get('index')
    reply_text = data.get('reply')
    if index is not None and 0 <= index < len(message_queue):
        message_queue[index]['reply'] = reply_text
        return jsonify({'status': 'Success'})
    return jsonify({'status': 'Error'}), 400

if __name__ == '__main__':
    app.run(debug=True)
