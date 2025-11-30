
# Smart Task Analyzer

A full-stack mini-application that analyzes tasks and intelligently prioritizes them using a custom scoring algorithm based on urgency, importance, effort, and dependencies.

## 🚀 Project Overview
The Smart Task Analyzer helps users determine **what to work on first** by computing a priority score for each task.  
The backend is powered by **Django**, while the frontend uses **HTML, CSS, and JavaScript** to provide an interactive UI.

---

## 📂 Project Structure
```
task-analyzer/
├── backend/
│   ├── settings.py
│   ├── urls.py
│   ├── wsgi.py
│   └── asgi.py
├── tasks/
│   ├── models.py
│   ├── scoring.py
│   ├── views.py
│   ├── urls.py
│   └── tests.py
├── frontend/
│   ├── index.html
│   ├── script.js
│   └── styles.css
├── manage.py
├── sample.json
├── requirements.txt
└── README.md
```

---

## ⚙️ Installation & Setup

### 1. Clone the repository
```bash
git clone https://github.com/yourusername/task-analyzer.git
cd task-analyzer
```

### 2. Create & activate virtual environment
```bash
python -m venv venv
venv\Scripts\activate
```

### 3. Install dependencies
```bash
pip install -r requirements.txt
```

### 4. Apply migrations & start backend
```bash
python manage.py migrate
python manage.py runserver
```

### 5. Start frontend server (static)
```bash
cd frontend
python -m http.server 8001
```

Open in browser:
```
http://localhost:8001/index.html
```

---

## 🧠 Scoring Algorithm Explanation

The algorithm computes a weighted priority score using the following factors:

### **1️⃣ Urgency**
- Overdue tasks receive a **large boost (+200)**.
- Due within 3 days → high boost.
- Due within 7 days → medium boost.
- Far deadlines → small or neutral.

### **2️⃣ Importance (1–10)**
Weighted directly:
```
importance × 10
```

### **3️⃣ Effort**
- ≤ 2 hours → quick-win bonus.
- Higher effort tasks → slight penalty.

### **4️⃣ Dependencies**
- If a task **blocks others**, score increases.
- If a task **is blocked by dependencies**, score decreases.
- Circular dependency → detected & penalized.

### **5️⃣ Strategy Modes**
Supports:
- **smart** (default)
- **fastest**
- **highimpact**
- **deadline**

---

## 🔌 API Endpoints

### **POST /api/tasks/analyze/**
Analyze and score tasks.

#### Example:
```bash
curl -X POST "http://127.0.0.1:8000/api/tasks/analyze/" -H "Content-Type: application/json" -d @sample.json
```

### **GET /api/tasks/suggest/**
Returns top 3 tasks.

---

## 🧪 Running Tests
```bash
python manage.py test
```

---

## 📘 Sample Input (sample.json)
```json
[
  {
    "id": 1,
    "title": "Fix login bug",
    "due_date": "2025-11-30",
    "estimated_hours": 3,
    "importance": 8,
    "dependencies": []
  }
]
```

---

## 🛠️ Technologies Used
- **Python, Django**
- **HTML, CSS, JavaScript**
- **Django CORS Headers**
- **JSON-based APIs**

---

## 📝 Future Enhancements
- Dependency graph visualization
- Weekend/holiday-aware urgency
- Machine learning-based prioritization
- Custom weight tuning per user

---

## 👨‍💻 Author
**Vavilala Krishna Murthi**  
GitHub: https://github.com/krishna111809  
LinkedIn: https://www.linkedin.com/in/krishna-murthi-vavilala/

