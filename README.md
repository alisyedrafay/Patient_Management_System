🏥 Patient Management System – FastAPI

A Patient Management System built using FastAPI & Python, providing RESTful APIs to manage patient records with full CRUD operations, sorting, and data validation.

This project demonstrates clean backend architecture and REST API best practices.

🚀 Features

Home & About endpoints

Add, view, update, and delete patients

View single or all patient records

Sort patients by attributes (e.g., name, age)

Input validation using Pydantic

Auto-generated API docs with Swagger UI

🛠 Tech Stack

Backend: FastAPI

Language: Python

Validation: Pydantic

Server: Uvicorn

📌 API Endpoints
Method	Endpoint	Description
GET	/	Home endpoint
GET	/about	About API
POST	/patients	Add new patient
GET	/patients	View all patients
GET	/patients/{id}	View patient by ID
PUT	/patients/{id}	Update patient
DELETE	/patients/{id}	Delete patient
GET	/patients/sort	Sort patients
▶️ How to Run
1️⃣ Install dependencies
pip install fastapi uvicorn

2️⃣ Run the server
uvicorn main:app --reload

3️⃣ Open API Docs
http://127.0.0.1:8000/docs

🎯 Purpose

Learn FastAPI fundamentals

Practice RESTful API development

Perform CRUD operations

Backend project for portfolio & freelancing

📂 Project Structure (Example)
patient-management-system/
│
├── main.py
├── models.py
├── routes/
├── README.md
└── .gitignore
