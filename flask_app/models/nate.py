from flask_app.config.db import query_db


class Nate:
    def __init__(self, data):
        self.id = data['id']
        self.first_name = data['first_name']
        self.last_name = data['last_name']
        self.email = data['email']
        self.comment = data['comment']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']

    @classmethod
    def get_all(cls):
        rows = query_db("SELECT * FROM comments ORDER BY created_at DESC;")
        return [cls(row) for row in rows]

    @classmethod
    def save(cls, data):
        query = """
            INSERT INTO comments (first_name, last_name, email, comment)
            VALUES (%(fname)s, %(lname)s, %(email)s, %(comment)s)
            RETURNING id;
        """
        row = query_db(query, data, fetch="one")
        return row['id']

    @classmethod
    def get_one(cls, data):
        row = query_db("SELECT * FROM comments WHERE id = %(user_id)s;", data, fetch="one")
        return cls(row) if row else None
