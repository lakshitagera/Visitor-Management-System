# Visitor Management System (VMS)

![Python](https://img.shields.io/badge/Python-3.x-blue.svg)
![Frappe](https://img.shields.io/badge/Frappe-Framework-green.svg)
![License](https://img.shields.io/badge/License-MIT-orange.svg)
![Status](https://img.shields.io/badge/Status-Development-success.svg)

A modern **Visitor Management System (VMS)** built on the **Frappe Framework** using **Python** and **JavaScript**. This application replaces traditional paper-based visitor logbooks with a secure digital visitor management solution.

---

## 📖 Table of Contents

- About
- Features
- Business Objectives
- Tech Stack
- System Workflow
- User Roles
- Project Structure
- Installation
- Configuration
- Usage
- Reports
- Security
- Screenshots
- Future Enhancements
- Contributing
- License

---

# 📌 About

The Visitor Management System (VMS) digitizes the complete visitor lifecycle from registration to checkout while providing secure approvals, badge generation, notifications, audit logs, and reporting.

The application is designed for organizations that need secure visitor tracking, host approval workflows, and real-time monitoring.

---

# ✨ Features

## Visitor Registration

- Walk-in Visitor Registration
- Online Pre-registration
- Visitor Photo Capture
- Government ID Verification
- Vehicle Information
- NDA Acknowledgement

---

## Approval Workflow

- Host Approval
- Reject Visitor
- Approval Reminder
- Escalation Workflow
- Email Notifications
- SMS Notifications (Optional)

---

## Visitor Check-In

- Real-time Queue
- Identity Verification
- Automatic Timestamp
- Badge Printing
- QR Code Generation

---

## Visitor Check-Out

- Scan Badge
- Automatic Checkout Time
- Visit Duration Calculation
- Overstay Detection

---

## Dashboard

Real-time dashboard displaying

- Pre-Registered
- Pending Approval
- Approved
- Rejected
- Checked-In
- Checked-Out
- Expired
- Overstay

---

## Reports

- Daily Visitor Report
- Visitor History
- Frequent Visitors
- Overstay Report
- Host Activity Report

Export reports to:

- CSV
- Excel

---

# 🎯 Business Objectives

- Eliminate paper visitor logbooks
- Improve reception efficiency
- Enhance facility security
- Host approval automation
- Real-time visitor tracking
- Accurate audit records
- Digital notifications

---

# 👥 User Roles

| Role | Responsibilities |
|-------|------------------|
| Admin | Manage system configuration, users, reports |
| Receptionist | Register visitors |
| Security | Check-In / Check-Out / Badge Printing |
| Host | Approve or Reject visitors |
| Visitor | Pre-register and receive visitor badge |

---

# 🔄 System Workflow

## Walk-In Visitor

Visitor
↓

Reception Registration
↓

Host Approval
↓

Security Check-In
↓

Badge Generation
↓

Meeting
↓

Check-Out
↓

Visit Closed

---

## Pre-Registration

Visitor / Host

↓

Online Registration

↓

Host Approval

↓

Arrival

↓

QR Verification

↓

Check-In

↓

Badge Printing

↓

Check-Out

---

# 🛠 Tech Stack

## Backend

- Python
- Frappe Framework

## Frontend

- JavaScript
- HTML
- CSS

## Database

- MariaDB

## Server

- Bench
- Nginx
- Redis

---

# 📂 Project Structure

```
visitor_management/

│

├── visitor_management/

│ ├── visitor/

│ ├── doctype/

│ ├── reports/

│ ├── dashboard/

│ ├── notifications/

│ ├── templates/

│ ├── public/

│ └── config/

│

├── patches/

├── fixtures/

├── hooks.py

├── modules.txt

├── requirements.txt

└── README.md
```

---

# 🚀 Installation

## Clone Repository

```bash
git clone https://github.com/yourusername/visitor-management.git
```

Move to project

```bash
cd visitor-management
```

Create App

```bash
bench new-app visitor_management
```

Install App

```bash
bench --site your-site install-app visitor_management
```

Run Server

```bash
bench start
```

---

# ⚙ Configuration

Configure:

- Email Account
- Notification Templates
- User Roles
- Badge Layout
- Approval Timeout
- Escalation Rules

---

# 📷 Visitor Badge

Badge contains

- Visitor Name
- Visitor Photo
- Host Name
- Department
- Visit Purpose
- QR Code
- Badge Number
- Check-in Time
- Expiry Date

---

# 🔐 Security

- AES-256 Encryption
- Role-Based Access Control (RBAC)
- Audit Logs
- Session Timeout
- Secure Authentication

---

# 📊 Reports

Available reports include:

- Daily Visitors
- Monthly Visitors
- Visitor History
- Frequent Visitors
- Overstay Visitors
- Host Analytics

---

# 📈 Performance

- Registration page loads within 2 seconds
- Dashboard refreshes every 5 seconds
- Badge generation under 3 seconds
- 99.5% uptime target

---

# 🚧 Future Enhancements

- Mobile Application
- Facial Recognition
- HRMS Integration
- Multi-Branch Support
- Biometric Authentication
- Visitor Self-Service Kiosk

---

# 🤝 Contributing

Contributions are welcome!

1. Fork the repository

2. Create your feature branch

```bash
git checkout -b feature/new-feature
```

3. Commit your changes

```bash
git commit -m "Added new feature"
```

4. Push to your branch

```bash
git push origin feature/new-feature
```

5. Create a Pull Request

---

# 📄 License

This project is licensed under the MIT License.

---

# 👨‍💻 Author

Your Name

GitHub: https://github.com/yourusername

LinkedIn: https://linkedin.com/in/yourprofile

---

## ⭐ Support

If you found this project useful, don't forget to give it a ⭐ on GitHub.
