from fastapi import FastAPI
from app.api.simulate import router as simulate_router
from app.database import engine
from app.models.simulation import Simulation
from app.database import Base
from app.api.history import router as history_router
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse
from app.api.auth import router as auth_router


Base.metadata.create_all(bind=engine)

app = FastAPI(title="Email Risk Simulator")
app.include_router(auth_router)
app.include_router(simulate_router)
app.include_router(history_router)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/favicon.ico", include_in_schema=False)
def favicon():
    return FileResponse("favicon.ico")