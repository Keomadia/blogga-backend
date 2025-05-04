from config import db


class Blog(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    title = db.Column(db.String(80), nullable=False)
    description = db.Column(db.String(225), nullable=False)
    media_url = db.Column(db.String(255), nullable=True)
    video_url = db.Column(db.String(255), nullable=True)
    tag = db.Column(db.String(50), nullable=True)
    authors_name = db.Column(db.String, nullable=False)
    date = db.Column(db.Date, nullable=True)
    views = db.Column(db.Integer, default=0)
    likes = db.Column(db.Integer, default=0)
    dislikes = db.Column(db.Integer, default=0)

    def to_json(self):
        return {
            "id": self.id,
            "title": self.title,
            "description": self.description,
            "media": self.media_url,
            "video": self.video_url,
            "tag": self.tag,
            "authors": self.authors_name,
            "date": self.date.isoformat() if self.date else None,
            "sections": [section.to_json() for section in self.sections if section.blog_id == self.id],
            "views": self.views,
            "likes": self.likes,
            "dislikes": self.dislikes,
        }

class Section(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    blog_id = db.Column(db.Integer, db.ForeignKey('blog.id'), nullable=False)
    section_title = db.Column(db.String(80), nullable=True)
    section_content = db.Column(db.Text, nullable=True)
    section_img = db.Column(db.String(255), nullable=True)
    section_list = db.Column(db.JSON, nullable=True)

    def to_json(self):
        return {
            "id": self.id,
            "blog_id": self.blog_id,
            "title": self.section_title,
            "content": self.section_content,
            "image": self.section_img,
            "list": self.section_list,
        }

Blog.sections = db.relationship('Section', backref='blog', lazy=True)

class Subscribers(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    email = db.Column(db.String(120), unique=True, nullable=False)
    
    def to_json(self):
        return {
            "id": self.id,
            "email": self.email,
    
        }
