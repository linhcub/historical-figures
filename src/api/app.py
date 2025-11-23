from fastapi import FastAPI
from api.routes.figure import router as figure_router

app = FastAPI()

@app.get("/")
async def root():
    return {"message": "FastAPI is running!"}

app.include_router(figure_router)
