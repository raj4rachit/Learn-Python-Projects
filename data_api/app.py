import os
from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
import pymysql
from urllib.parse import quote_plus

from sqlalchemy.exc import SQLAlchemyError

app = Flask(__name__)

username = 'rachit'
password = quote_plus('Tbs@519@root')
database = 'test_api'
host = '192.168.1.218'

app.config['SQLALCHEMY_DATABASE_URI'] = f'mysql+pymysql://{username}:{password}@{host}/{database}'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)


class FAQS(db.Model):
    post_id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(80), nullable=False)
    content = db.Column(db.Text, nullable=False)
    category_id = db.Column(db.Integer, db.ForeignKey('categories.post_id'), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    def to_dict(self):
        return {
            "post_id": self.post_id,
            "title": self.title,
            "content": self.content,
            "category_id": self.category_id,
            "created_at": self.created_at.isoformat()
        }

class CATEGORIES(db.Model):
    post_id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(150), nullable=False)
    slug = db.Column(db.String(200), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    def cto_dict(self):
        return {
            "post_id": self.post_id,
            "name": self.name,
            "slug": self.slug,
            "created_at": self.created_at.isoformat()
        }

class BLOG(db.Model):
    post_id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(80), nullable=False)
    content = db.Column(db.Text, nullable=False)
    category_id = db.Column(db.Integer, db.ForeignKey('categories.post_id'), nullable=False)
    banner_image = db.Column(db.String(200), nullable=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    def to_dict(self):
        return {
            "post_id": self.post_id,
            "title": self.title,
            "content": self.content,
            "category_id": self.category_id,
            "banner_image": self.banner_image,
            "created_at": self.created_at.isoformat()
        }


@app.route('/api/faqs', methods=['POST'])
def add_faq():
    data = request.get_json()
    if not data or 'title' not in data or 'content' not in data:
        return jsonify({'message': 'Title and Content are required'}), 400

    # Check for an optional post_id in the data to decide if updating is required
    post_id = data.get('post_id')
    try:
        if post_id:
            # Attempt to find an existing FAQ by post_id
            faq = FAQS.query.filter_by(post_id=post_id).first()
            if faq:
                # If found, update the existing faq
                faq.title = data['title']
                faq.content = data['content']
                faq.category_id = data.get('category_id')
                db.session.commit()
                print(faq.to_dict())
                return jsonify({'message': 'FAQ updated', 'faq': faq.to_dict()}), 200
            else:
                # If no post_id or post_id is None, create a new FAQ entry
                new_faq = FAQS(post_id=data['post_id'],title=data['title'], content=data.get('content', ''),category_id=data['category_id'])
                db.session.add(new_faq)
                db.session.commit()
                print(new_faq.to_dict())
                return jsonify({'message': 'FAQ added', 'faq': faq.to_dict()}), 201
        else:
            # If not found, send a 404 error
            return jsonify({'message': 'FAQ not found'}), 404
    except SQLAlchemyError as e:
        # Handle general SQLAlchemy errors
        db.session.rollback()
        print(e)
        return jsonify({'message': 'Database error', 'error': str(e)}), 500
    except Exception as e:
        # Handle unexpected errors
        print(e)
        return jsonify({'message': 'Server error', 'error': str(e)}), 500


@app.route('/api/faqs', methods=['GET'])
def get_faqs():
    faqs = FAQS.query.all()
    return jsonify([faq.to_dict() for faq in faqs]), 200


@app.route('/api/delete/faq/<int:post_id>', methods=['DELETE'])
def delete_faq(post_id):
    # Attempt to find the FAQ by post_id
    faq = FAQS.query.filter_by(post_id=post_id).first()

    if faq:
        # If FAQ is found, delete it from the database
        db.session.delete(faq)
        db.session.commit()
        return jsonify({'message': 'FAQ deleted successfully'}), 200
    else:
        # If no FAQ is found with the given id, return a 404 error
        return jsonify({'message': 'FAQ not found'}), 404

@app.route('/api/faq/<int:post_id>', methods=['GET'])
def get_faq_detail(post_id):
    # Find the FAQ by post_id
    faq = FAQS.query.filter_by(post_id=post_id).first()
    if faq:
        return jsonify([faq.to_dict()]), 200
    else:
        return jsonify({'message': 'FAQ not found'}), 404

#----------- Category -----------------#

@app.route('/api/category', methods=['POST'])
def add_category():
    data = request.get_json()
    if not data or 'name' not in data or 'slug' not in data:
        return jsonify({'message': 'Name & slug are required'}), 400

    # Check for an optional post_id in the data to decide if updating is required
    post_id = data.get('post_id')
    try:
        if post_id:
            # Attempt to find an existing FAQ by post_id
            category = CATEGORIES.query.filter_by(post_id=post_id).first()
            if category:
                # If found, update the existing faq
                category.name = data['name']
                category.slug = data['slug']
                db.session.commit()
                print(category.cto_dict())
                return jsonify({'message': 'Category updated', 'faq': category.cto_dict()}), 200
            else:
                # If no post_id or post_id is None, create a new FAQ entry
                new_category = CATEGORIES(post_id=data['post_id'],name=data['name'], slug=data.get('slug'))
                db.session.add(new_category)
                db.session.commit()
                print(new_category.cto_dict())
                return jsonify({'message': 'Category added', 'category': category.cto_dict()}), 201
        else:
            # If not found, send a 404 error
            return jsonify({'message': 'Category not found'}), 404
    except SQLAlchemyError as e:
        # Handle general SQLAlchemy errors
        db.session.rollback()
        return jsonify({'message': 'Database error', 'error': str(e)}), 500
    except Exception as e:
        # Handle unexpected errors
        return jsonify({'message': 'Server error', 'error': str(e)}), 500

@app.route('/api/categories', methods=['GET'])
def get_categories():
    categories = CATEGORIES.query.all()
    return jsonify([category.cto_dict() for category in categories]), 200

@app.route('/api/category/delete/<int:post_id>', methods=['DELETE'])
def delete_category(post_id):
    # Attempt to find the FAQ by post_id
    category = CATEGORIES.query.filter_by(post_id=post_id).first()

    if category:
        # If FAQ is found, delete it from the database
        db.session.delete(category)
        db.session.commit()
        return jsonify({'message': 'Category deleted successfully'}), 200
    else:
        # If no FAQ is found with the given id, return a 404 error
        return jsonify({'message': 'Category not found'}), 404


#----------- Blogs -----------------#

@app.route('/api/blogs', methods=['POST'])
def add_blog():
    data = request.get_json()
    if not data or 'title' not in data or 'content' not in data:
        return jsonify({'message': 'Title and Content are required'}), 400

    # Check for an optional post_id in the data to decide if updating is required
    post_id = data.get('post_id')
    try:
        if post_id:
            # Attempt to find an existing Blog by post_id
            blog = BLOG.query.filter_by(post_id=post_id).first()
            if blog:
                # If found, update the existing blog
                blog.title = data['title']
                blog.content = data['content']
                blog.category_id = data.get('category_id')
                blog.banner_image = data.get('image_url')
                db.session.commit()
                print(blog.to_dict())
                return jsonify({'message': 'Blog updated', 'blog': blog.to_dict()}), 200
            else:
                # If no post_id or post_id is None, create a new blog entry
                new_blog = BLOG(post_id=data['post_id'],title=data['title'],category_id=data['category_id'],banner_image=data['image_url'], content=data.get('content', ''))
                db.session.add(new_blog)
                db.session.commit()
                print(new_blog.to_dict())
                return jsonify({'message': 'Blog added', 'blog': blog.to_dict()}), 201
        else:
            # If not found, send a 404 error
            return jsonify({'message': 'Blog not found'}), 404
    except SQLAlchemyError as e:
        # Handle general SQLAlchemy errors
        db.session.rollback()
        return jsonify({'message': 'Database error', 'error': str(e)}), 500
    except Exception as e:
        # Handle unexpected errors
        return jsonify({'message': 'Server error', 'error': str(e)}), 500

@app.route('/api/blog', methods=['GET'])
def get_blogs():
    blogs = BLOG.query.all()
    return jsonify([blog.to_dict() for blog in blogs]), 200


@app.route('/api/delete/blog/<int:post_id>', methods=['DELETE'])
def delete_blog(post_id):
    # Attempt to find the blog by post_id
    blog = BLOG.query.filter_by(post_id=post_id).first()

    if blog:
        # If Blog is found, delete it from the database
        db.session.delete(blog)
        db.session.commit()
        return jsonify({'message': 'Blog deleted successfully'}), 200
    else:
        # If no FAQ is found with the given id, return a 404 error
        return jsonify({'message': 'Blog not found'}), 404

@app.route('/api/blog/<int:post_id>', methods=['GET'])
def get_blog_detail(post_id):
    # Find the FAQ by post_id
    blog = BLOG.query.filter_by(post_id=post_id).first()
    if blog:
        return jsonify([blog.to_dict()]), 200
    else:
        return jsonify({'message': 'Blog not found'}), 404


@app.route('/')
def index():
    return "Welcome to the API"


if __name__ == '__main__':
    #db.create_all()
    app.run(host='0.0.0.0', port=5000, debug=True)
