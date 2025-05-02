from flask import request , jsonify 
from models import *
from datetime import datetime
from config import app, db
from dotenv import load_dotenv
load_dotenv()



# POST
@app.route('/api/blog/new', methods=['POST'])
def create_blog_post():
    data = request.get_json()
    if not data:
        return jsonify({"error": "No data provided"}), 400
    try:
        blog = Blog(
            title=data.get('title'),
            description=data.get('description'),
            media_url=data.get('media_url'),
            video_url=data.get('video_url'),
            tag=data.get('tag'),
            authors_name=data.get('authors_name'),
            date=datetime.now(),
            views=data.get('views', 0),
            likes=data.get('likes', 0),
            dislikes=data.get('dislikes', 0)
        )
        db.session.add(blog)
        db.session.commit()
        
        sections = data.get('sections', [])
        for section_data in sections:
            section = Section(
            blog_id=blog.id,  # Now blog.id will have a value
            section_title=section_data.get('section_title'),
            section_content=section_data.get('section_content'),
            section_img=section_data.get('section_img'),
            section_list=section_data.get('section_list')
            )
            db.session.add(section)
        
        db.session.commit()
        return jsonify({"message": "Blog post created successfully"}), 201
    except Exception as e:
        db.session.rollback()
        return jsonify({"error": str(e)}), 500

@app.route('/api/blog/all', methods=['GET'])
def get_blog_post():
    try:
        blogs = Blog.query.all()
        blog_list = []
        for blog in blogs:
            blog_list.append(blog.to_json())
            
        return jsonify(blog_list), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500
    
@app.route('/api/blog/<int:blog_id>', methods=['GET'])
def get_blog_post_by_id(blog_id):
    try:
        blog = Blog.query.get_or_404(blog_id)
        return jsonify({
            'id': blog.id,
            'title': blog.title,
            'description': blog.description,
            'media_url': blog.media_url,
            'video_url': blog.video_url,
            'tag': blog.tag,
            'authors_name': blog.authors_name,
            'date': blog.date,
            'views': blog.views,
            'likes': blog.likes,
            'dislikes': blog.dislikes
        }), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@app.route('/api/blog/delete/<int:blog_id>', methods=['DELETE'])
def delete_blog_post(blog_id):
    try:
        blog = Blog.query.get_or_404(blog_id)
        db.session.delete(blog)
        db.session.commit()
        return jsonify({"message": "Blog post deleted successfully"}), 200
    except Exception as e:
        db.session.rollback()
        return jsonify({"error": str(e)}), 500
    
@app.route('/api/blog/update/<int:blog_id>', methods=['PUT'])
def update_blog_post(blog_id):
    data = request.get_json()
    if not data:
        return jsonify({"error": "No data provided"}), 400
    try:
        blog = Blog.query.get_or_404(blog_id)
        blog.title = data.get('title', blog.title)
        blog.description = data.get('description', blog.description)
        blog.media_url = data.get('media_url', blog.media_url)
        blog.video_url = data.get('video_url', blog.video_url)
        blog.views = data.get('views', blog.views)
        blog.likes = data.get('likes', blog.likes)
        blog.dislikes = data.get('dislikes', blog.dislikes)
        blog.tag = data.get('tag', blog.tag)
        blog.authors_name = data.get('authors_name', blog.authors_name)
        db.session.commit()
        
        sections = data.get('sections', [])
        for section_data in sections:
            section = Section(
                blog_id=blog.id,
                section_title=section_data.get('section_title'),
                section_content=section_data.get('section_content'),
                section_img=section_data.get('section_img'),
                section_list=section_data.get('section_list')
            )
            db.session.add(section)
        
        db.session.commit()
        return jsonify({"message": "Blog post updated successfully"}), 200
    except Exception as e:
        db.session.rollback()
        return jsonify({"error": str(e)}), 500  
  
@app.route('/api/blog/subscribe', methods=['POST'])
def subscribe():
    data = request.get_json()
    if not data or 'email' not in data:
        return jsonify({"error": "No email provided"}), 400
    try:
        email = data['email']
        if Subscribers.query.filter_by(email=email).first():
            return jsonify({"message": "Already subscribed"}), 200
        
        subscriber = Subscribers(email=email)
        db.session.add(subscriber)
        db.session.commit()
        return jsonify({"message": "Subscribed successfully"}), 201
    except Exception as e:
        db.session.rollback()
        return jsonify({"error": str(e)}), 500
    

@app.route('/api/blog/unsubscribe/<int:subscriber_id>', methods=['DELETE'])
def unsubscribe(subscriber_id):
    try:
        subscriber = Subscribers.query.get_or_404(subscriber_id)
        db.session.delete(subscriber)
        db.session.commit()
        return jsonify({"message": "Unsubscribed successfully"}), 200
    except Exception as e:
        db.session.rollback()
        return jsonify({"error": str(e)}), 500



@app.route('/api/blog/subscribers', methods=['GET'])
def get_subscribers():
    try:
        subscribers = Subscribers.query.all()
        subscriber_list = [subscriber.to_json() for subscriber in subscribers]
        return jsonify(subscriber_list), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500
    
@app.route('/api/blog/<int:blog_id>/section/all', methods=['GET'])
def get_all_sections(blog_id):
    try:
        sections = Section.query.filter_by(blog_id=blog_id)
        section_list = []
        for section in sections:
            section_list.append(section.to_json())        
        return jsonify(section_list), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/api/blog/<int:blog_id>/<int:section_id>', methods=['GET'])
def get_section(blog_id,section_id):
    try:
        section = Section.query.filter_by(id=section_id)
        section_list = [sect.to_json() for sect in section]
        return jsonify(section_list), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500



@app.route('/api/blog/<int:blog_id>/<int:section_id>/update', methods=['PUT'])
def update_section(blog_id,section_id):
    data = request.get_json()
    if not data:
        return jsonify({"error": "No data provided"}), 400
    try:
        section = Section.query.filter_by(id=section_id, blog_id=blog_id).first_or_404()
        section.section_title = data.get('section_title', section.section_title)
        section.section_content = data.get('section_content', section.section_content)
        section.section_img = data.get('image', section.section_img)
        section.section_list = data.get('section_list', section.section_list)
        db.session.commit()
        return jsonify({"message": "Section updated successfully"}), 200
    except Exception as e:
        db.session.rollback()
        return jsonify({"error": str(e)}), 500

@app.route('/api/blog/<int:blog_id>/<int:section_id>/delete', methods=['DELETE'])
def delete_section(blog_id, section_id):
    try:
        section = Section.query.filter_by(id=section_id, blog_id=blog_id).first_or_404()
        db.session.delete(section)
        db.session.commit()
        return jsonify({"message": "Section deleted successfully"}), 200
    except Exception as e:
        db.session.rollback()
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True)
    
    
    

example_json = {
    "title": "Flask Guide : Setting Up Flask and Creating Your First App",
    "description": "A detailed guide to setting up Flask, covering installation, configuration, and creating your first app.",
    "media_url": "https://flask.palletsprojects.com/en/stable/_images/flask-horizontal.png",
    "video_url": "https://www.youtube.com/embed/VY4n3ij45as",
    "tag": "Tech",
    "sections": [
        {
            "section_title": "Flask Setup",
            "section_content": "Flask is a lightweight web framework for Python, ideal for beginners and experienced developers. Learn its key features.",
            "section_img": None,
            "section_list": [
                {"Why Flask?": "Flask is simple, flexible, and powerful, making it great for small projects and APIs."},
                {"Features": "Flask supports routing, templates, and extensions for added functionality."},
                {"Use Cases": "Flask is perfect for small projects, RESTful APIs, and microservices."}
            ]
        },
        {
            "section_title": "Installing Flask",
            "section_content": "Learn how to install Flask using pip, set up a virtual environment, and verify the installation.",
            "section_img": "https://media.geeksforgeeks.org/wp-content/uploads/20220425112216/A.png",
            "section_list": [
                {"Step 1": "Install Python 3.6 or higher."},
                {"Step 2": "Create a virtual environment using 'python -m venv env'."},
                {"Step 3": "Activate the virtual environment."},
                {"Step 4": "Run 'pip install Flask' to install Flask."},
                {"Step 5": "Verify installation with 'flask --version'."}
            ]
        },
        {
            "section_title": "First Flask App",
            "section_content": "Create a basic Flask app, define routes, and run it locally to see it in action.",
            "section_img": None,
            "section_list": [
                {"Step 1": "Create a Python file (e.g., 'app.py')."},
                {"Step 2": "Import Flask and initialize the app."},
                {"Step 3": "Define routes using '@app.route'."},
                {"Step 4": "Run the app locally with 'python app.py'."},
                {"Step 5": "Access the app at 'http://127.0.0.1:5000/'."}
            ]
        },
        {
            "section_title": "Directory Structure",
            "section_content": "Organize your Flask project for scalability using a recommended directory structure.",
            "section_img": "https://i.sstatic.net/UpYLa.png",
            "section_list": [
                {"Static Folder": "Store CSS, JavaScript, and images."},
                {"Templates Folder": "Store HTML files for rendering."},
                {"Config File": "Use 'config.py' for app settings."},
                {"Modular Code": "Separate routes, models, and configurations."}
            ]
        },
        {
            "section_title": "Next Steps",
            "section_content": "Explore advanced Flask topics and resources to enhance your skills and build complex applications.",
            "section_img": None,
            "section_list": [
                {"Extensions": "Learn Flask-SQLAlchemy and Flask-Migrate."},
                {"Templating": "Explore Flask's Jinja2 templating engine."},
                {"APIs": "Build RESTful APIs with Flask."},
                {"Resources": "Read the official Flask documentation and tutorials."}
            ]
        },
        {
            "section_title": "Final Thoughts",
            "section_content": "Flask is a versatile framework that empowers developers to build robust web applications with ease. By mastering its core features and exploring advanced topics, you can create scalable and efficient solutions. Keep learning, experimenting, and leveraging Flask's ecosystem to bring your ideas to life.",
            "section_img": None,
            "section_list": None
        }
    ],
    "authors_name": "Dominic Doe",
    "views": 0,
    "likes": 0,
    "dislikes": 0
}

 