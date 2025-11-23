from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from api.routes.figure import router as figure_router

app = FastAPI()

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # In production, replace with specific origins
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
async def root():
    return {"message": "FastAPI is running!"}

app.include_router(figure_router)
