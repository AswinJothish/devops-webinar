from flask import Flask, render_template, request, redirect, url_for, flash, send_from_directory
from werkzeug.utils import secure_filename
from datetime import datetime
import os
import uuid

app = Flask(__name__)
app.secret_key = 'your-secret-key-change-in-production'

# Configuration
UPLOAD_FOLDER = 'static/uploads'
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif', 'webp'}
MAX_FILE_SIZE = 5 * 1024 * 1024  # 5MB

app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['MAX_CONTENT_LENGTH'] = MAX_FILE_SIZE

# Create upload folder if it doesn't exist
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

# In-memory todos with enhanced structure
todos = []

def allowed_file(filename):
    """Check if file extension is allowed"""
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        todo_text = request.form.get('todo')
        priority = request.form.get('priority', 'medium')
        category = request.form.get('category', 'general')
        
        # Handle file upload
        image_filename = None
        if 'image' in request.files:
            file = request.files['image']
            if file and file.filename and allowed_file(file.filename):
                # Generate unique filename
                ext = file.filename.rsplit('.', 1)[1].lower()
                image_filename = f"{uuid.uuid4().hex}.{ext}"
                file.save(os.path.join(app.config['UPLOAD_FOLDER'], image_filename))
        
        if todo_text:
            todo = {
                'id': len(todos) + 1,
                'text': todo_text,
                'completed': False,
                'priority': priority,
                'category': category,
                'image': image_filename,
                'created_at': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
                'updated_at': None
            }
            todos.append(todo)
            flash('Task added successfully!', 'success')
            return redirect(url_for('index'))
    
    # Get filter parameters
    filter_priority = request.args.get('priority', 'all')
    filter_category = request.args.get('category', 'all')
    filter_status = request.args.get('status', 'all')
    
    # Filter todos
    filtered_todos = todos
    if filter_priority != 'all':
        filtered_todos = [t for t in filtered_todos if t['priority'] == filter_priority]
    if filter_category != 'all':
        filtered_todos = [t for t in filtered_todos if t['category'] == filter_category]
    if filter_status == 'completed':
        filtered_todos = [t for t in filtered_todos if t['completed']]
    elif filter_status == 'pending':
        filtered_todos = [t for t in filtered_todos if not t['completed']]
    
    # Calculate statistics
    stats = {
        'total': len(todos),
        'completed': len([t for t in todos if t['completed']]),
        'pending': len([t for t in todos if not t['completed']]),
        'high_priority': len([t for t in todos if t['priority'] == 'high' and not t['completed']]),
        'categories': len(set(t['category'] for t in todos))
    }
    
    return render_template('index.html', 
                         todos=filtered_todos, 
                         all_todos=todos,
                         stats=stats,
                         filter_priority=filter_priority,
                         filter_category=filter_category,
                         filter_status=filter_status)

@app.route('/toggle/<int:todo_id>')
def toggle(todo_id):
    """Toggle task completion status"""
    for todo in todos:
        if todo['id'] == todo_id:
            todo['completed'] = not todo['completed']
            todo['updated_at'] = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            flash(f"Task {'completed' if todo['completed'] else 'reopened'}!", 'success')
            break
    return redirect(url_for('index'))

@app.route('/edit/<int:todo_id>', methods=['GET', 'POST'])
def edit(todo_id):
    """Edit an existing task"""
    todo = next((t for t in todos if t['id'] == todo_id), None)
    if not todo:
        flash('Task not found!', 'error')
        return redirect(url_for('index'))
    
    if request.method == 'POST':
        todo['text'] = request.form.get('todo', todo['text'])
        todo['priority'] = request.form.get('priority', todo['priority'])
        todo['category'] = request.form.get('category', todo['category'])
        todo['updated_at'] = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        
        # Handle new image upload
        if 'image' in request.files:
            file = request.files['image']
            if file and file.filename and allowed_file(file.filename):
                # Delete old image if exists
                if todo['image']:
                    old_image_path = os.path.join(app.config['UPLOAD_FOLDER'], todo['image'])
                    if os.path.exists(old_image_path):
                        os.remove(old_image_path)
                
                # Save new image
                ext = file.filename.rsplit('.', 1)[1].lower()
                image_filename = f"{uuid.uuid4().hex}.{ext}"
                file.save(os.path.join(app.config['UPLOAD_FOLDER'], image_filename))
                todo['image'] = image_filename
        
        flash('Task updated successfully!', 'success')
        return redirect(url_for('index'))
    
    return render_template('edit.html', todo=todo)

@app.route('/delete/<int:todo_id>')
def delete(todo_id):
    """Delete a task"""
    global todos
    todo = next((t for t in todos if t['id'] == todo_id), None)
    if todo:
        # Delete associated image if exists
        if todo['image']:
            image_path = os.path.join(app.config['UPLOAD_FOLDER'], todo['image'])
            if os.path.exists(image_path):
                os.remove(image_path)
        
        todos = [t for t in todos if t['id'] != todo_id]
        flash('Task deleted successfully!', 'success')
    return redirect(url_for('index'))

@app.route('/delete-image/<int:todo_id>')
def delete_image(todo_id):
    """Delete image from a task"""
    todo = next((t for t in todos if t['id'] == todo_id), None)
    if todo and todo['image']:
        image_path = os.path.join(app.config['UPLOAD_FOLDER'], todo['image'])
        if os.path.exists(image_path):
            os.remove(image_path)
        todo['image'] = None
        todo['updated_at'] = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        flash('Image removed successfully!', 'success')
    return redirect(url_for('index'))

@app.route('/clear')
def clear():
    """Clear all tasks"""
    global todos
    # Delete all images
    for todo in todos:
        if todo['image']:
            image_path = os.path.join(app.config['UPLOAD_FOLDER'], todo['image'])
            if os.path.exists(image_path):
                os.remove(image_path)
    todos = []
    flash('All tasks cleared!', 'success')
    return redirect(url_for('index'))

@app.route('/uploads/<filename>')
def uploaded_file(filename):
    """Serve uploaded files"""
    return send_from_directory(app.config['UPLOAD_FOLDER'], filename)

@app.route('/health')
def health():
    """Health check endpoint for container orchestration"""
    return {
        'status': 'healthy',
        'todos_count': len(todos),
        'completed_count': len([t for t in todos if t['completed']]),
        'timestamp': datetime.now().isoformat()
    }, 200

@app.errorhandler(413)
def too_large(e):
    """Handle file too large error"""
    flash('File is too large! Maximum size is 5MB.', 'error')
    return redirect(url_for('index'))

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port, debug=True)
