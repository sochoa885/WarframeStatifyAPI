import asyncio
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from apscheduler.schedulers.background import BackgroundScheduler

from config.warframe_data import fetch_and_update_items

fetch_hours = 6

app = FastAPI(
    title="WarframeStatifyAPI",
    description="A tool that collects information from warframe.market",
    version="1.0.0"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["GET, HEAD"],
    allow_headers=["*"],
)

@app.on_event("startup")
async def startup():
    start_scheduler()
    asyncio.create_task(fetch_and_update_items())


def start_scheduler():
    scheduler = BackgroundScheduler()
    scheduler.add_job(lambda: asyncio.run(fetch_and_update_items()), 'interval', hours=fetch_hours)
    scheduler.start()