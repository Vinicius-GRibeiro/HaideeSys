# HaideeSys

![Python](https://img.shields.io/badge/Python-3.11+-3776AB?logo=python)
![Flet](https://img.shields.io/badge/Flet-Desktop-blue)
![PostgreSQL](https://img.shields.io/badge/PostgreSQL-Database-336791?logo=postgresql)

HaideeSys is a desktop Academic Management System developed with **Python**, **Flet** and **PostgreSQL**.

The project aims to centralize school administration by providing tools for student management, attendance tracking, academic records and disciplinary events, following a modular software architecture.

It was designed as a real-world application to practice software engineering concepts, database modeling and desktop application development.

---

# Features

- Student management
- Academic grade management
- Attendance tracking
- Student scoring system
- Incident registration
- User authentication *(planned)*
- Audit logging
- PostgreSQL persistence
- Modular architecture

---

# Tech Stack

- Python
- Flet
- PostgreSQL
- Peewee ORM
- python-dotenv
- Object-Oriented Programming
- Git

---

# Main Features

## Student Management

Manage student information through a complete CRUD workflow.

Features include:

- Register students
- Update information
- Search records
- Student score tracking

---

## Academic Series

Create and organize academic classes.

The module supports:

- Creating new classes
- Listing existing classes
- Linking students to classes

---

## Attendance Management

Manage daily attendance records.

Capabilities include:

- Attendance registration
- Attendance history
- Student presence tracking

---

## Incident Management

Register and manage disciplinary or academic incidents.

Each occurrence stores:

- Student
- Date
- Subject
- Description

The system also allows filtering by:

- Student
- Class
- Occurrence ID

---

## Logging

The application automatically records important events.

Different log files are maintained for:

- General information
- Errors
- Development/debugging

This facilitates troubleshooting and system auditing.

---

# Database

The application uses PostgreSQL with Peewee ORM.

Main entities include:

- Students
- Academic Classes
- Attendance
- Incidents
- Scores

Relationships are mapped using ORM models.

---

# Project Structure

The project follows a modular organization that separates:

- User Interface
- Business Logic
- Database Layer
- Logging
- Application Services

---

# Installation

Clone the repository.

```bash
git clone https://github.com/Vinicius-GRibeiro/HaideeSys.git
```

Install dependencies.

```bash
pip install -r requirements.txt
```

Configure the environment.

```env
DBNAME=...
DBUSER=...
DBPASSWORD=...
DBHOST=...
DBPORT=5432
```

Run the application.

```bash
python main.py
```

---

# Roadmap

- Authentication system
- User roles
- Dashboard
- Grade reports
- PDF export
- Student history
- Parent portal
- Backup & Restore
- Docker support
- Automated tests

---

# Skills Demonstrated

This project demonstrates experience with:

- Python
- Desktop Application Development
- PostgreSQL
- Peewee ORM
- Database Modeling
- CRUD Operations
- Object-Oriented Programming
- Software Architecture
- Logging Systems
- Layered Architecture
- Data Persistence
- Environment Variables

---
