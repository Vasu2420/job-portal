# Job Portal

A web-based **Job Portal** built with **Flask (Python)** and **MySQL**.  
It provides a platform where **employers** can post jobs and **candidates** can search and apply for them.

---

## 🚀 Features

- 👤 **User Authentication** – Register & login system for candidates and employers  
- 💼 **Job Posting** – Employers can create, edit, and delete job postings  
- 🔎 **Job Search** – Candidates can browse available jobs  
- 📝 **Job Application** – Candidates can apply for jobs directly  
- 🗄 **Database Integration** – Data stored securely in MySQL  
- 📱 **Responsive UI** – Built with HTML, CSS, Bootstrap  

---

## 🛠 Tech Stack

- **Frontend:** HTML, CSS, Bootstrap  
- **Backend:** Python (Flask)  
- **Database:** MySQL  
- **Templating:** Jinja2  

---

## ⚙️ Installation & Setup

1. **Clone the repository**
   ```bash
   git clone https://github.com/Vasu2420/job-portal.git
   cd job-portal
1.python -m venv venv
venv\Scripts\activate   # On Windows
source venv/bin/activate   # On Mac/Linux
2.pip install flask mysql-connector-python
3.Create a MySQL database (e.g., job_portal)

Update app.py with your MySQL username and password

Run SQL scripts (if any) to create tables
4.python app.py
5.open in browser http://127.0.0.1:5000/



job-portal/
│── app.py              # Flask backend
│── requirements.txt    # Dependencies
│── templates/          # HTML templates
│   ├── index.html
│   ├── login.html
│   ├── register.html
│── static/             # CSS, JS, images
│   ├── style.css
│── README.md           # Project documentation



