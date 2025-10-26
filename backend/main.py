from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS

# --- Initialize Flask App ---
app = Flask(__name__)
CORS(app)

# --- Database Configuration ---
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///comments.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

# --- Database Model ---
class Comment(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    text = db.Column(db.String(200), nullable=False)
    task_id = db.Column(db.Integer, nullable=True)  # Added task_id

# --- Create Database Tables ---
with app.app_context():
    db.create_all()

# --- Root Route ---
@app.route('/')
def home():
    return jsonify({"message": "Flask Comment API is running 🚀"})

# --- CRUD Routes ---
@app.route('/comments/<int:task_id>', methods=['GET'])
def get_comments(task_id):

@app.route('/comments', methods=['POST'])
def add_comment():
    data = request.get_json()
    if not data or 'text' not in data:
        return jsonify({"error": "No comment text provided"}), 400
    
    task_id = data.get('task_id', None)
    new_comment = Comment(text=data['text'], task_id=task_id)
    db.session.add(new_comment)
    db.session.commit()
    return jsonify({"message": "Comment added!"}), 201

@app.route('/comments/<int:id>', methods=['PUT'])
def edit_comment(id):
    data = request.get_json()
    comment = Comment.query.get(id)
    if not comment:
        return jsonify({'error': 'Comment not found'}), 404

    comment.text = data.get('text', comment.text)
    db.session.commit()
    return jsonify({'message': 'Comment updated successfully'})

@app.route('/comments/<int:id>', methods=['DELETE'])
def delete_comment(id):
    comment = Comment.query.get(id)
    if not comment:
        return jsonify({'error': 'Comment not found'}), 404

    db.session.delete(comment)
    db.session.commit()
    return jsonify({'message': 'Comment deleted successfully'})

# --- Run Server ---
if __name__ == '__main__':
    app.run(debug=True)
