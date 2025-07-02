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
- **Tables Used**:
  - `users` – Stores user credentials
  - `resumes` – Stores resume text or uploads
  - `skills` – Stores list of skills per user
  - `jobs` – Job entries with required skills

## 🚀 How to Run the Project

1. **Clone the Repository**:
   ```bash
   git clone [https://github.com/yourusername/skill-job-matching.git](https://github.com/kavananagaraj03/SkillBasedJobMatching.git)
   cd SkillBasedJobMatching
   python main.py
