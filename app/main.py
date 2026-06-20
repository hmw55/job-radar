from fastapi import FastAPI

app = FastAPI(
    title="Job Radar",
    version="0.5.0",
    description="A respectful job aggregation and alerting engine.",
)

@app.get("/health")
async def health_check() -> dict[str, str]:
    return {"status": "ok"}