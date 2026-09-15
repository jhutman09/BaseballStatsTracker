from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.routers import club, season, team

app = FastAPI(title="Baseball Stats Tracker")

# Vite's default dev server port. Adjust/extend once the frontend exists.
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/health")
def health_check():
    return {"status": "ok"}


app.include_router(club.router)
app.include_router(season.router)
app.include_router(team.router)

# Routers get wired up here as we build them, e.g.:
# from app.routers import players, games, stats
# app.include_router(players.router)
# app.include_router(games.router)
# app.include_router(stats.router)
