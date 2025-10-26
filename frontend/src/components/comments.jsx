import { useState, useEffect } from "react";

function Comments({ taskId }) {
  const [comments, setComments] = useState([]);
  const [commentText, setCommentText] = useState("");
  const [editingId, setEditingId] = useState(null);
  const [editingText, setEditingText] = useState("");

  const API_URL = "http://127.0.0.1:5000"; // Your Flask backend URL

  // Fetch comments
  const fetchComments = async () => {
    try {
      const res = await fetch(`${API_URL}/comments/${taskId}`);
      const data = await res.json();
      setComments(data);
    } catch (err) {
      console.error("Error fetching comments:", err);
    }
  };

  useEffect(() => {
    fetchComments();
  }, [taskId]);

  // Add new comment
  const handleAddComment = async () => {
    if (!commentText.trim()) return;
    try {
      const res = await fetch(`${API_URL}/comments`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ text: commentText, task_id: taskId }),
      });
      if (!res.ok) throw new Error("Failed to add comment");
      setCommentText("");
      fetchComments();
    } catch (err) {
      console.error(err);
    }
  };

  // Start editing a comment
  const startEditing =(id, text) => {
    setEditingId(id);
    setEditingText(text);
  };

  // Save edited comment
  const handleEditComment = async (id) => {
    try {
      const res = await fetch(`${API_URL}/comments/${id}`, {
        method: "PUT",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ text: editingText }),
      });
      if (!res.ok) throw new Error("Failed to update comment");
      setEditingId(null);
      setEditingText("");
      fetchComments();
    } catch (err) {
      console.error(err);
    }
  };

  // Delete comment
  const handleDeleteComment = async (id) => {
    try {
      const res = await fetch(`${API_URL}/comments/${id}`, {
        method: "DELETE",
      });
      if (!res.ok) throw new Error("Failed to delete comment");
      fetchComments();
    } catch (err) {
      console.error(err);
    }
  };

  return (
    <div style={{ maxWidth: "500px", margin: "0 auto" }}>
      <h2>Comments</h2>

      <ul>
        {comments.map((c) => (
          <li key={c.id} style={{ marginBottom: "8px" }}>
            {editingId === c.id ? (
              <>
                <input
                  value={editingText}
                  onChange={(e) => setEditingText(e.target.value)}
                />
                <button onClick={() => handleEditComment(c.id)}>Save</button>
                <button onClick={() => setEditingId(null)}>Cancel</button>
              </>
            ) : (
              <>
                <span>{c.text}</span>
                <button onClick={() => startEditing(c.id, c.text)}>Edit</button>
                <button onClick={() => handleDeleteComment(c.id)}>Delete</button>
              </>
            )}
          </li>
        ))}
      </ul>

      <input
        type="text"
        value={commentText}
        onChange={(e) => setCommentText(e.target.value)}
        placeholder="Add comment"
        style={{ width: "70%", marginRight: "8px" }}
      />
      <button onClick={handleAddComment}>Add</button>
    </div>
  );
}

export default Comments;
