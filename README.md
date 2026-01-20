# TryHup

TryHup is an experimental, creator-focused social platform designed to explore
alternative growth, engagement, and content quality metrics, going beyond
traditional likes and raw view counts.

The project is built as a technical MVP to experiment with modern full-stack
architectures, database-driven governance, and scalable moderation workflows.

---

## 🚀 Vision

Most social platforms optimize for:
- volume
- virality
- noise

TryHup explores a different approach, where:
- growth is measurable
- engagement is structured
- quality can be analyzed, not guessed
- creators receive meaningful feedback, not just vanity metrics

---

## 🧱 Architecture

TryHup is organized as a monorepo:

TryHup/
├── tryhup-backend/ # Backend API (Python)
├── tryhup-frontend/ # Frontend web app (React / Vite)
├── database/ # Database schema (Supabase / PostgreSQL)
│ └── schema.sql
└── README.md

yaml
Copy code

Each layer is intentionally separated to ensure clarity, scalability, and maintainability.

---

## ⚙️ Tech Stack

### Backend
- Python
- FastAPI
- Supabase (PostgreSQL)
- Role-based access control
- Content moderation services

### Frontend
- React
- Vite
- Component-driven UI
- API-first architecture

### Database
- PostgreSQL (Supabase)
- Versioned schema (`database/schema.sql`)
- Structured relations for users, content, interactions, and moderation

---

## 🗄️ Database Schema

The database structure is publicly available and versioned in:

database/schema.sql

yaml
Copy code

The file contains only the database structure (tables and relations).
No real data or credentials are included.

---

## 📌 Project Status

Early-stage technical MVP under active development.

TryHup currently serves as:
- a full-stack experimentation platform
- a system design and architecture showcase
- a personal portfolio project

---

## 🧠 Author

Angelo Saffo

Background in IT operations and technical environments,
with a degree in Law, and currently studying Computer Engineering
and Artificial Intelligence, with a strong interest in software
architecture and full-stack development.

---

## 📄 License

This project is released under the MIT License
and is intended for educational and experimental use.
