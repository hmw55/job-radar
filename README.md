# Job Radar

## Overview

Job Radar is an automated job discovery platform that continuously monitors company application tracking systems (ATS), identifies opportunities matching a personalized search profile, and delivers real-time notifications through Discord.

Rather than searching traditional job boards, Job Radar connects directly to company hiring systems, allowing opportunities to be discovered as soon as they are published. 


Currently supports:
- Greenhouse
- Lever
- Ashby

and includes automated source discovery, PostgreSQL persistence, match scoring, Discord notifications, and scheduled execution through GitHub Actions.

---

## Why I Built It

Finding software engineering jobs oftem means checking dozens of company career pages every day. 

Most job boards:
- Lag behind company ATS systems
- Aggregate duplicate listings
- Lack meaningful filtering
- Require constant manual searching

Job Radar was built to automate that process. 

Instead of checking company career pages manually, the system continuously polls ATS providers, evaluates new opportunities against a customizable search profile, and sends notifications only for relevant positions.

---

## Key Features

### Multi-ATS Ingestion

Polls multiple applicant tracking systems through a unifies souce interface:
- Greenhouse
- Lever
- Ashby

Additional providers can be added without changing the ingestion pipeline.

### Automated Source Discovery

Job Radar can discover company ATS providers automatically.

Given a company slug: 
```text
vercel
```

The discovery engine attempts:
```text
Greenhouse
Lever
Ashby
``` 

and automatically registers successful sources inside the company registry.

### Match Scoring Engine

Jobs are scored against a configurable profile using:
- Preferred titiles
- Technical Keywords
- Experience level matching
- Remote eligibility
- Location preferences
- Exclusion filters

Example:

```text
Software Engineer
Score: 90
Level: Excellent Match
```

### Discord Notifications

High-scoring opportunities are delivered directly to Discord using webjooks. 

Features include:
- Duplicate prevention
- Notification history tracking
- Configurable rate limites
- Match reasoning summaries

### Source Registry

Discovered sources are stored in PostgreSQL/Supabase.

New sources can be:
- Added manually
- Imported for CSV
- Registered through discovery

without required application code changes.

---

## Architecture 

```
GitHub Actions Scheduler
            │
            ▼
      Job Radar Runner
            │
            ▼
     Source Discovery
            │
            ▼
      Company Registry
            │
            ▼
      ATS Providers
      ├── Greenhouse
      ├── Lever
      └── Ashby
            │
            ▼
      Job Ingestion
            │
            ▼
       PostgreSQL
            │
            ▼
     Match Scoring
            │
            ▼
   Discord Notifications
```

---

## Technical Stack

### Backend 
- Python 3.14
- AsyncIO
- HTTPX

### Database
- PostgreSQL
- Supabase
- SQLAlchemy
- Alembic

### Automation
- GitHub Actions

### Quality
- Ruff
- MyPy

---

## Current Scale

Current Development environment:

```text
ATS Providers: 3
Sources Monitored: 13
Jobs Tracked: 1,000+
Notification Channel: Discord
Database: PostrgeSQL
```

---
## Roadmap

### Near Term
- Additional ATS providers
- Expanded source discovery
- Improved ranking algorithms
- Better remote location filtering

### Long Term
- Integration into JobSearchingSucks.com
    - Web dashboard
    - Multi-user support
    - Analytics and reporting


---

## See the Wiki for detailed setup instructions, database schema, and source disovery internals.