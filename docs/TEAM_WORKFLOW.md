# Team Workflow

## Team Members

### Person 1

AI / Computer Vision

### Person 2

Backend / Database

### Person 3

Frontend / GIS

---

# GitHub

Use ONE repository:

urban-intelligence-platform

---

# Branches

main
ai-dev
backend-dev
frontend-dev

---

# Branch Rules

Do not directly experiment on main.

Each person works on their own branch.

---

# Development Process

1. Pull latest main.
2. Switch to your own branch.
3. Implement your assigned feature.
4. Test locally.
5. Commit changes.
6. Push your branch.
7. Create a Pull Request.
8. Team reviews.
9. Merge into main.

---

# Integration Order

First:

AI
↓
Event JSON
↓
FastAPI
↓
Database
↓
Frontend
↓
GIS Map

---

# First Integration Milestone

The first complete working flow must be:

Video
↓
AI detects pothole
↓
AI creates Event JSON
↓
POST /events
↓
FastAPI
↓
PostgreSQL
↓
GET /events
↓
React
↓
Pothole appears on GIS map

Only after this works should advanced features be added.

---

# ChatGPT Usage Rule

Each team member may use ChatGPT to help develop their assigned module.

However, ChatGPT must NOT independently redesign:

- Architecture
- API contract
- Database structure
- Technology stack
- Folder structure

The shared project documentation is the source of truth.

If ChatGPT suggests a major architectural change, discuss it with the team before implementing it.
