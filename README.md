# 🚀 DevOps Todo App - Professional Edition

A feature-rich, production-ready todo application built with Flask, designed for DevOps webinars and demonstrations. Includes image uploads, advanced filtering, priority management, and complete CRUD operations.

![Version](https://img.shields.io/badge/version-2.0-blue)
![Python](https://img.shields.io/badge/python-3.11+-green)
![Flask](https://img.shields.io/badge/flask-3.0-red)
![License](https://img.shields.io/badge/license-MIT-yellow)

## ✨ Key Features

### 📝 Task Management
- ✅ **Create, Read, Update, Delete** tasks
- 🎯 **Priority Levels**: Low, Medium, High with visual indicators
- 📂 **Categories**: General, Work, Personal, Shopping, Health, Learning
- ✔️ **Task Completion** toggle with visual feedback
- 🕒 **Timestamps**: Creation and last update tracking

### 🖼️ Image Attachments
- 📸 **Upload Images** to tasks (PNG, JPG, GIF, WebP)
- 🗑️ **Remove Images** from tasks individually
- 🔍 **Image Preview** with modal zoom view
- 💾 **Max 5MB** per image with validation
- 🎨 **Responsive thumbnails** in task cards

### 🎨 Professional UI/UX
- 🌈 **Modern gradient design** with smooth animations
- 📊 **Statistics Dashboard** showing task metrics
- 🔔 **Flash Messages** for user feedback
- 📱 **Fully Responsive** design for all devices
- 🎯 **Priority color coding** (Red/Yellow/Green)
- 🌓 **Clean, professional aesthetics**

### 🔍 Advanced Filtering
- 📋 **Filter by Status**: All, Pending, Completed
- 🎯 **Filter by Priority**: All, Low, Medium, High
- 📂 **Filter by Category**: All categories available
- 🔄 **Combine filters** for precise task views
- 🧮 **Live task counts** with filter results

### 🛠️ DevOps Features
- 🐳 **Docker containerization** ready
- 🏥 **Health check endpoint** (`/health`)
- 📦 **Docker Compose** configuration
- 🔧 **Environment variables** support
- 🎯 **Production-ready** structure
- 📝 **Comprehensive logging**

## 🚀 Quick Start

### Local Development

1. **Clone or download the project files**

2. **Install dependencies:**
```bash
pip install -r requirements.txt
```

3. **Run the application:**
```bash
python app.py
```

4. **Open your browser:**
```
http://localhost:5000
```

### Docker Deployment

1. **Build and run with Docker Compose:**
```bash
docker-compose up --build
```

2. **Or use Docker manually:**
```bash
# Build image
docker build -t devops-todo-app .

# Run container
docker run -p 5000:5000 -v $(pwd)/static/uploads:/app/static/uploads devops-todo-app
```

## 📁 Project Structure

```
devops-todo-app/
│
├── app.py                      # Main Flask application
├── requirements.txt            # Python dependencies
├── Dockerfile                  # Container configuration
├── docker-compose.yml          # Multi-container setup
├── .dockerignore              # Docker build exclusions
├── README.md                  # This file
│
├── templates/
│   ├── index.html             # Main task list page
│   └── edit.html              # Task editing page
│
├── static/
│   ├── style.css              # Modern CSS styling
│   └── uploads/               # Image upload directory (auto-created)
│
└── .gitignore                 # Git exclusions
```

## 🔌 API Endpoints

| Endpoint | Method | Description |
|----------|--------|-------------|
| `/` | GET/POST | Main todo list page, add new tasks |
| `/edit/<id>` | GET/POST | Edit existing task |
| `/toggle/<id>` | GET | Toggle task completion status |
| `/delete/<id>` | GET | Delete a task and its image |
| `/delete-image/<id>` | GET | Remove image from task |
| `/clear` | GET | Clear all tasks and images |
| `/health` | GET | Health check endpoint (JSON) |
| `/uploads/<filename>` | GET | Serve uploaded images |

## 🎯 Usage Examples

### Adding a Task with Image
1. Enter task description
2. Select priority and category
3. Click "Attach Image" and choose a file
4. Click "Add Task"

### Editing a Task
1. Click the edit icon (✏️) on any task
2. Modify text, priority, or category
3. Optionally upload a new image
4. Click "Save Changes"

### Filtering Tasks
1. Use the filter section to select criteria
2. Filters combine: Status + Priority + Category
3. Task count updates automatically
4. Click "All" to clear individual filters

### Image Management
- **View full size**: Click on any task image
- **Remove image**: Click the X button on the image
- **Replace image**: Edit the task and upload new image

## ⚙️ Configuration

### Environment Variables

```bash
# Server Port
PORT=5000

# Flask Environment
FLASK_ENV=development  # or production

# Secret Key (change in production!)
SECRET_KEY=your-secret-key-here
```

### Upload Settings

Modify in `app.py`:
```python
UPLOAD_FOLDER = 'static/uploads'
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif', 'webp'}
MAX_FILE_SIZE = 5 * 1024 * 1024  # 5MB
```

### Customization

**Change Colors** - Edit CSS variables in `static/style.css`:
```css
:root {
    --primary-color: #3b82f6;
    --success-color: #10b981;
    --warning-color: #f59e0b;
    --danger-color: #ef4444;
}
```

**Add Categories** - Update both files:
- `templates/index.html` (form select options)
- `templates/edit.html` (form select options)

## 🐳 Docker Configuration

### Dockerfile Features
- Python 3.11 slim base image
- Optimized layer caching
- Health check configuration
- Non-root user execution
- Volume mount for uploads

### Docker Compose
- Auto-restart on failure
- Volume persistence for images
- Environment variable injection
- Port mapping configuration

## 📊 Statistics Dashboard

The app tracks and displays:
- **Total Tasks**: All tasks created
- **Completed**: Tasks marked as done
- **Pending**: Tasks still to do
- **High Priority**: Urgent pending tasks
- **Categories**: Number of unique categories

## 🔒 Security Features

- ✅ File upload validation (type and size)
- ✅ Secure filename generation (UUID)
- ✅ Flash message authentication
- ✅ CSRF protection ready
- ✅ SQL injection safe (no DB in demo)
- ✅ XSS prevention in templates

## 🎓 DevOps Webinar Topics

This app demonstrates:

1. **Containerization**
   - Dockerfile best practices
   - Multi-stage builds potential
   - Volume management

2. **Health Monitoring**
   - `/health` endpoint
   - Container health checks
   - Readiness probes

3. **File Management**
   - Upload handling
   - Storage persistence
   - Cleanup strategies

4. **State Management**
   - Session handling
   - Data persistence options
   - Scaling considerations

5. **UI/UX Patterns**
   - Flash messages
   - Form validation
   - Responsive design

## 🚀 Deployment Options

### Heroku
```bash
# Add Procfile
echo "web: python app.py" > Procfile

# Deploy
heroku create my-todo-app
git push heroku main
```

### AWS Elastic Beanstalk
```bash
eb init -p python-3.11 todo-app
eb create todo-app-env
eb open
```

### Google Cloud Run
```bash
gcloud run deploy todo-app --source . --allow-unauthenticated
```

### Kubernetes
Example deployment in `/k8s/` directory (see deployment.yaml)

## 🔄 Database Migration Path

To add database persistence:

1. **Choose database**: PostgreSQL, MySQL, or MongoDB
2. **Install ORM**: SQLAlchemy or PyMongo
3. **Replace** in-memory `todos` list
4. **Add** database connection config
5. **Create** migration scripts
6. **Update** Docker Compose with DB service

Example with PostgreSQL:
```python
from flask_sqlalchemy import SQLAlchemy

app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://user:pass@localhost/todos'
db = SQLAlchemy(app)

class Todo(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    text = db.Column(db.String(500), nullable=False)
    # ... other fields
```

## 📝 Future Enhancements

Potential additions:
- [ ] User authentication and multi-user support
- [ ] Database integration (PostgreSQL/MongoDB)
- [ ] RESTful API with JWT authentication
- [ ] WebSocket for real-time updates
- [ ] Task due dates and reminders
- [ ] Drag-and-drop task reordering
- [ ] Task sharing and collaboration
- [ ] Email notifications
- [ ] Dark mode toggle
- [ ] Export tasks to CSV/PDF
- [ ] Task search functionality
- [ ] Subtasks and checklists
- [ ] Tags in addition to categories
- [ ] Activity log/history
- [ ] Mobile app (React Native/Flutter)

## 🤝 Contributing

Contributions are welcome! Here's how:

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add AmazingFeature'`)
4. Push to branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## 📄 License

MIT License - Feel free to use this for your webinars, demos, and projects!

## 🙏 Acknowledgments

- Flask framework and community
- Modern CSS techniques and best practices
- DevOps community for inspiration
- All contributors and users

## 📞 Support

For issues, questions, or suggestions:
- Open an issue on GitHub
- Email: your-email@example.com
- Twitter: @yourhandle

---

**Made with ❤️ for DevOps professionals and learners**

*Perfect for demonstrations of: containerization, CI/CD pipelines, cloud deployments, monitoring, logging, and modern web development practices.*
