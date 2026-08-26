```markdown
# Database Schema

Database:

PostgreSQL

ORM:

SQLAlchemy

---

# 1. buses

Stores information about buses.

Fields:

- id
- bus_id
- route
- latitude
- longitude
- status
- created_at
- updated_at

---

# 2. events

Stores AI-generated urban events.

Fields:

- id
- event_id
- event_type
- bus_id
- latitude
- longitude
- timestamp
- confidence
- evidence
- created_at

---

# 3. incidents

Stores vehicle incidents.

Fields:

- id
- incident_id
- vehicle_number
- confidence
- bus_id
- latitude
- longitude
- timestamp
- evidence
- created_at

---

# 4. traffic_records

Stores traffic information.

Fields:

- id
- location
- latitude
- longitude
- vehicle_count
- average_speed
- traffic_level
- timestamp

---

# 5. pedestrian_hotspots

Stores repeated pedestrian-risk observations.

Fields:

- id
- location
- latitude
- longitude
- observation_count
- peak_time
- risk_level
- created_at

---

# Database Rules

Use PostgreSQL.

Use SQLAlchemy for database interaction.

Use Pydantic models for API validation.

Do not introduce another database unless the team agrees.
```
