from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.routers import batting_line, club, game, pitching_appearance, player, roster, roster_entry, season, stats

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


app.include_router(batting_line.router)
app.include_router(club.router)
app.include_router(game.router)
app.include_router(pitching_appearance.router)
app.include_router(player.router)
app.include_router(roster.router)
app.include_router(roster_entry.router)
app.include_router(season.router)
app.include_router(stats.router)

# Routers get wired up here as we build them, e.g.:
# from app.routers import stats
# app.include_router(stats.router)
