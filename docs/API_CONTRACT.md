# API Contract

Version: 1.0

This document defines how the AI, backend and frontend communicate.

All team members must follow this contract.

---

# 1. Base Backend URL

Development:

http://127.0.0.1:8000

FastAPI documentation:

http://127.0.0.1:8000/docs

---

# 2. AI → Backend Event

The AI module sends detected events to:

POST /events

---

## Request Body

```json
{
  "event_type": "pothole",
  "bus_id": "BUS101",
  "latitude": 13.0478,
  "longitude": 80.257,
  "timestamp": "2026-08-26T10:42:17",
  "confidence": 0.94,
  "evidence": "frame_1042.jpg"
}
```
