<h1 align=center>
Job Radar
</h1>

<p align=center>
Job Radar is a respectful job aggregation and alerting engine that monitors public job sources and ATS providers for new roles, stores them, filters them through configurable search profiles, and sends notifications. 
</p>

---

## Goals

- Use public endpoints and structure feeds where possible 
- Avoid auth bypassing, CAPTCHA bypassing, auto-apply flows, or spammy scraping
- Support configurable search profiles
- Start with SQLite, later support POstgreSQL
- Start with Discord notifications, later support multiple notification channels

## Tech Stack

- Python 3.14+
- FastAPI
- SQLAlchemy
- APScheduler
- HTTPX
- Discord webhooks

## Local Development

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -e ".[dev]"
uvicorn app.main:app --reload
```