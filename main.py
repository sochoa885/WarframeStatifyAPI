from config.app_config import app
from database.database import Base, engine
from routes import tags, types, items

Base.metadata.create_all(bind=engine)

app.include_router(tags.router)
app.include_router(types.router)
app.include_router(items.router)

@app.get("/", description="", summary="")
async def get_warframe_items():
    return "API ON"

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000, reload=True)