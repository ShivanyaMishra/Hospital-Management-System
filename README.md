# Hospital-Management-System
This project is a UI-enhanced Hospital Management System designed to manage patient details and prescription records efficiently.
The backend logic and database structure remain intact, while the interface has been rebuilt using CustomTkinter to provide a professional, modern, and user-friendly experience.

The system allows hospital staff to add, update, delete, view, search, and preview prescriptions and patient data stored in a MySQL database.

##✨ Key Features
🎨 Modern UI (CustomTkinter)

Dark mode (default) & Light mode toggle

Clean layout with responsive panels

Scrollable forms for large data input

Consistent typography and spacing

🧾 Patient & Prescription Management

Store patient details (ID, name, DOB, gender, address)

Manage prescription information:

Tablet name

Disease

Dose & daily dose

Issue & expiry dates

Side effects & storage advice

Auto-filled form on row selection

🗄 Database Integration (MySQL)

Full CRUD operations:

Insert prescription data

Fetch and display records

Update existing records

Delete records safely

Uses mysql-connector-python

Error handling for database failures

🔍 Search & Filter

Real-time search across:

Tablet name

Patient name

Reference number

Dynamically filters TreeView data

📊 Data Table (TreeView)

Scrollable, styled table

Displays all hospital records

Click-to-load record into form

Clean column formatting

👁 Prescription Preview

Generates formatted prescription text

Displays details in a preview panel

Useful for printing or verification

🧭 Navigation & Controls

Refresh button to reload data

Clear form button

Delete with confirmation

Safe exit dialog

🛠 Tech Stack
Component	Technology
Language	Python 3.10+
GUI	CustomTkinter + Tkinter
Database	MySQL
DB Connector	mysql-connector-python
Architecture	Class-based (OOP)
📂 Project Structure
Hospital-Management-System/
│
├── hospital.py        # Main application (UI + DB logic)
└── README.md          # Project documentation

⚙️ Installation & Setup
1️⃣ Install Python

Download from:
👉 https://www.python.org/downloads/

2️⃣ Install Required Libraries
pip install customtkinter mysql-connector-python

3️⃣ Setup MySQL Database

Create a database named hospital and a table hospital_data with required columns (matching code fields).

Update DB credentials in code if needed:

host="localhost"
username="root"
password="***"
database="hospital"

4️⃣ Run the Application
python hospital.py

⌨️ Keyboard & UI Notes

Click any row to load data into the form

Search filters results live

Update/Delete requires selecting a record

Deletions are permanent

## ⚠ Important Notes

This project focuses on UI improvement, not database redesign

Database credentials are hardcoded (for learning/demo purposes)

No authentication system included

Always back up your database before testing delete operations

## 🔮 Future Improvements

Login & role-based access

Input validation & date pickers

Print/export prescriptions

Pagination for large datasets

Secure credential handling

REST API integration

## 📜 License

This project is provided as-is for educational and learning purposes.
Use responsibly in real-world environments.
