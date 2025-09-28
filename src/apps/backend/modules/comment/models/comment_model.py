from datetime import datetime
from modules.logger.logger import Logger

class Comment:
    _storage = []  # simple in-memory storage

    def __init__(self, task_id, content, author="Anonymous"):
        self.id = len(Comment._storage) + 1
        self.task_id = task_id
        self.content = content
        self.author = author
        self.created_at = datetime.utcnow()
        self.updated_at = datetime.utcnow()

    def to_dict(self):
        return {
            "id": self.id,
            "task_id": self.task_id,
            "content": self.content,
            "author": self.author,
            "created_at": self.created_at.isoformat(),
            "updated_at": self.updated_at.isoformat()
        }

    @classmethod
    def add(cls, comment):
        cls._storage.append(comment)
        Logger.info(f"Comment added: {comment.to_dict()}")
        return comment

    @classmethod
    def get_by_task(cls, task_id):
        return [c for c in cls._storage if c.task_id == task_id]

    @classmethod
    def update(cls, comment_id, content):
        for c in cls._storage:
            if c.id == comment_id:
                c.content = content
                c.updated_at = datetime.utcnow()
                return c
        return None

    @classmethod
    def delete(cls, comment_id):
        before = len(cls._storage)
        cls._storage = [c for c in cls._storage if c.id != comment_id]
        return len(cls._storage) < before
