from flask import Blueprint, request, jsonify
from modules.comment.models.comment_model import Comment

class CommentRestApiServer:
    @staticmethod
    def create():
        bp = Blueprint("comment_api", __name__)

        @bp.route("/api/tasks/<int:task_id>/comments", methods=["GET"])
        def list_comments(task_id):
            return jsonify([c.to_dict() for c in Comment.get_by_task(task_id)]), 200

        @bp.route("/api/tasks/<int:task_id>/comments", methods=["POST"])
        def add_comment(task_id):
            data = request.get_json()
            if not data or "content" not in data:
                return jsonify({"error": "Content required"}), 400
            comment = Comment(task_id, data["content"], data.get("author", "Anonymous"))
            Comment.add(comment)
            return jsonify(comment.to_dict()), 201

        @bp.route("/api/comments/<int:comment_id>", methods=["PATCH"])
        def edit_comment(comment_id):
            data = request.get_json()
            updated = Comment.update(comment_id, data.get("content"))
            if not updated:
                return jsonify({"error": "Comment not found"}), 404
            return jsonify(updated.to_dict())

        @bp.route("/api/comments/<int:comment_id>", methods=["DELETE"])
        def delete_comment(comment_id):
            ok = Comment.delete(comment_id)
            if not ok:
                return jsonify({"error": "Comment not found"}), 404
            return jsonify({"deleted": True})

        return bp
