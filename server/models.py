from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import validates
db = SQLAlchemy()

class Author(db.Model):
    __tablename__ = 'authors'
    
    id = db.Column(db.Integer, primary_key=True)
    name= db.Column(db.String, unique=True, nullable=False)
    phone_number = db.Column(db.String(10))
    created_at = db.Column(db.DateTime, server_default=db.func.now())
    updated_at = db.Column(db.DateTime, onupdate=db.func.now())

    @validates('name', 'phone_number')
    def validate_author(self, key, value):
        if key == 'name':
            if not value:
                raise ValueError("Name can not be empty and must be unique.")
            if Author.query.filter_by(name=value).first():
                raise ValueError("Name must be unique.")
            return value
    
        elif key == 'phone_number':
            if not value:
                raise ValueError("Phone number must be provided.")
            if len(value) != 10 or not value.isdigit():
                raise   ValueError("Phone number must be 10 digits.")
            return value

    def __repr__(self):
        return f'Author(id={self.id}, name={self.name})'

class Post(db.Model):
    __tablename__ = 'posts'
    
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String, nullable=False)
    content = db.Column(db.String)
    category = db.Column(db.String)
    summary = db.Column(db.String(250))
    created_at = db.Column(db.DateTime, server_default=db.func.now())
    updated_at = db.Column(db.DateTime, onupdate=db.func.now())

    allowed_categories =  ['Fiction', 'Non-Fiction']
    allowed_titles = ["Won't Beleive", "Secret", "Top", "Guess"]
    
    @validates('content')
    def validate_content(self, key, content_value):
        if not len(content_value) >= 250:
            raise ValueError("The post content MUST be atleast 250 characters long")
        
        return content_value

    @validates('summary')
    def validate_summary(self, key, summary_value):
        if len(summary_value) > 250:
            raise ValueError("Post summary should be a maximum of 250 characters")
        
        return summary_value
    
    @validates('category')
    def validate_category(self, key, category_type):
        if category_type != 'Fiction' and category_type != 'Non-Fiction':
            raise ValueError("Post category can only be either Fiction or Non-Fiction")
        
        return category_type
    
    @validates('title')
    def validate_title(self, key, post_title):
        clickbait_phrases = ["Won't Believe", "Secret", "Top", "Guess"]
        if not post_title or post_title.strip() == '':
            raise ValueError("Title CANNOT be empty")
        
        if not any(phrase in post_title for phrase in clickbait_phrases):
            raise ValueError("Your title is not click-baity")
        
        return post_title

    def __repr__(self):
        return f'Post(id={self.id}, title={self.title} content={self.content}, summary={self.summary})'
