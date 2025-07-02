# 🔍 Skill-Based Job Matching System

A web-based platform that matches users with suitable job opportunities based on the skills they submit in their resumes. New users can sign up, enter their resume details and skill sets, and get job recommendations tailored to their profile.

## 🌟 Features

- User Signup and Login
- Resume and Skills Submission
- Automatic Job Matching Based on Skills
- Job Listings from Database
- Responsive Frontend using HTML/CSS
- Backend-Powered Matching using Python

## 🛠️ Tech Stack

- **Frontend**: HTML, CSS
- **Backend**: Python (main.py)
- **Database**: MySQL (using XAMPP - phpMyAdmin)
- **Server**: Flask (or basic Python HTTP server)
- **Tools**: XAMPP for MySQL management

## 🧩 Database Schema

- **Database Name**: `p_job`
📊 Tables Used
users – Stores user credentials and personal details like name, email, password.

resumes – Stores uploaded resume data (text or file reference) linked to users.

skills – Contains a list of skills associated with each user.

jobs – Stores job entries along with required skills and job details.

company – Holds predefined company details including company name, job titles, and description.

courses – Lists additional courses or learning resources (with links) suggested based on user’s skills or job gaps.


## 🚀 How to Run the Project

1. **Clone the Repository**:
   ```bash
   git clone [https://github.com/yourusername/skill-job-matching.git](https://github.com/kavananagaraj03/SkillBasedJobMatching.git)
   cd SkillBasedJobMatching
Set Up Database:

Open XAMPP and start Apache and MySQL.

Go to http://localhost/phpmyadmin.

Create a database named p_job.

Import the .sql file (if you have one), or manually create tables (users, skills, jobs, etc.) as defined.

Run the Backend:

bash
Copy
Edit
python main.py
Access the Web App:
Open your browser and go to: http://localhost:5000 (or whatever port is set).

📁 Project Structure
php
Copy
Edit
project/
│
├── main.py                # Python backend logic and DB connections
├── templates/             # HTML files (login.html, signup.html, dashboard.html)
├── static/                # CSS, JS, images (if any)
└── README.md              # You're reading it!

🙋‍♂️ Author
Kavana Nagaraj
